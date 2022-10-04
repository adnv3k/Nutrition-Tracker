from wsgiref.simple_server import WSGIRequestHandler
import requests
import time
import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension
from django.core.cache import cache

from .models import Food, FoodHistory, SRLegacy, Branded
from .endpoints import Endpoints as ep
from .api import usda_key

class HomePageView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self):
        context = super(HomePageView, self).get_context_data()
        context['username'] = self.request.user.username
        return context

class SearchResultsView(ListView):
    model = Food
    template_name = 'search_results.html'
    paginate_by = 15
    brandOwner = False

    def get_context_data(self):
        """Override to return current user's username in the navbar
        """
        context = super(SearchResultsView, self).get_context_data()
        context['username'] = self.request.user.username
        return context

    def get_queryset(self):
        q = self.request.GET.get("q")
        if self.request.GET.get("brand"):
            dataType = 'Branded'
        else:
            dataType = 'SR Legacy'
        cached_string = f'{q}{dataType}'
        if cache.get(cached_string):
            return cache.get(cached_string)
        vector = SearchVector("name")
        query = SearchQuery(q)
        if dataType == 'Branded':
            food_q = Branded.objects.annotate(
                rank=SearchRank(vector, query), search=vector).filter(search=query).order_by('-rank')
        else:
            food_q = SRLegacy.objects.annotate(
                rank=SearchRank(vector, query), search=vector).filter(search=query).order_by('-rank')
        if len(food_q) <= 0:
            self.allow_empty = True
            return []
        elif food_q.exists():
            cache.set(cached_string, food_q, 60*5)
            return food_q
        else:
            return self.search(query, dataType)
            
    def search(self, query, data_type):
        end_search = ep().end_search(api_key=usda_key, query=query)
        params = end_search[1]
        url = end_search[0]
        params['dataType'] = data_type
        start = time.time()
        while True:
            try:
                food_query = requests.get(url, params=params, timeout=30)
                break
            except ConnectionError:
                if time.time() > start + 30:
                    raise Exception('Unable to reach USDA API after 30 seconds of connection errors.')
                else:
                    time.sleep(1)
        if len(food_query.json()) <= 0:
            self.allow_empty = True
            return []
        food_l = []
        for food in food_query.json():
            nutrients_unformat = food['foodNutrients']
            nutrients_clean = []
            name = [value['name'] for value in nutrients_unformat]
            amount = [value['amount'] for value in nutrients_unformat]
            unit = [value['unitName'] for value in nutrients_unformat]
            for name, amount, unit in zip(name, amount, unit):
                nutrients_clean.append("".join(f"{name}: {amount}{unit}"))
            food_l.append({'description': food['description'], 'foodNutrients': nutrients_clean})
            # if not Food.objects.filter(name=food_dict['food']['description']).exists():
            #    Food.objects.get_or_create(name=food_dict['food']['description'], nutrients=nutrients_clean)
            if data_type == 'Branded':
                brand_owner = food['brandOwner']
                Food.objects.get_or_create(
                    name=food['description'], nutrients=nutrients_clean,
                    dataType=params['dataType'], brandOwner=brand_owner)
            else:
                Food.objects.get_or_create(
                    name=food['description'], nutrients=nutrients_clean, dataType=params['dataType'])

        p = Paginator(Food.objects.all().filter(Q(name__icontains=[query])), 15)
        page_num = self.request.GET.get('page')
        page_obj = p.get_page(page_num)
        return render(self.request, 'search_results.html', {'page_obj': page_obj})
    


def add_food(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get('addBtn'):
                items = dict(request.POST.items())
                try:
                    fdc_id = int(SRLegacy.objects.filter(name=items['addBtn']).values('fdc_id')[0]['fdc_id'])
                except:
                    fdc_id = int(Branded.objects.filter(name=items['addBtn']).values('fdc_id')[0]['fdc_id'])
                FoodHistory.objects.get_or_create(username=items['username'],
                                                food=items['addBtn'],
                                                date=timezone.now(),
                                                fdc_id=fdc_id)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect('../login')

def favorite_food(request, pk):
    user = request.user
    if request.method == 'POST':
        if SRLegacy.objects.filter(id=pk).exists():
            food = get_object_or_404(SRLegacy, id=pk)
        else:
            food = get_object_or_404(Branded, id=pk)
        _favorited = user in food.favorite.all()
        if _favorited:
            food.favorite.remove(user)
            return HttpResponse('false')
        else:
            food.favorite.add(user)
            return HttpResponse('true')
# Migrate SR Legacy foods
# data = open("FoodData_Central_sr_legacy_food_json_2021-10-28.json")
# data = json.load(data)
# srlegacyfoods = data["SRLegacyFoods"]
# count = 0
# for entry in srlegacyfoods:
#     # Name
#     name = entry['description']

#     # Food Category
#     food_category = entry['foodCategory']['description']

#     # fdcId
#     fdc_id = entry['fdcId']
    
#     # Publication Date
#     publication_date = entry['publicationDate']
#     publication_date = publication_date.split('/')
#     for i, n in enumerate(publication_date):
#         publication_date[i] = int(n)
#     year = publication_date[2]
#     day = publication_date[1]
#     if day < 10:
#         day = f'0{day}'
#     month = publication_date[0]    
#     if month < 10:
#         month = f'0{month}'
#     publication_date = f'{year}-{month}-{day}'

#     # Nutrients
#     nutrient_list = []
#     for nutriententry in entry['foodNutrients']:
#         element = ""
#         nutrient_name = nutriententry['nutrient']['name']
#         id = str(nutriententry['nutrient']['id'])
#         amount = str(nutriententry['amount'])
#         unitname = nutriententry['nutrient']['unitName']
#         if unitname == "Âµg":
#             unitname = 'ug'
#         element = f'{nutrient_name} ({id}): {amount}{unitname}'
#         nutrient_list.append(element)
#     nutrient_list.sort()

#     SRLegacy.objects.create(
#         name=name,
#         category=food_category,
#         fdc_id=fdc_id,
#         publication_date=publication_date,
#         nutrients=nutrient_list
#     )
#     count += 1
#     print(f'Finished SRLegacy: {count}')

# Migrate Branded foods
# data = open("FoodData_Central_branded_food_json_2022-04-28.json", encoding='mbcs')
# data = json.load(data)
# brandedfoods = data["BrandedFoods"]
# count = 0
# for entry in brandedfoods:
#     # Brand name
#     brandOwner = entry['brandOwner']

#     # Name
#     name = entry['description']

#     # fdcId
#     fdc_id = entry['fdcId']

#     # Food Category
#     food_category = entry['brandedFoodCategory']
    
#     # Publication Date
#     publication_date = entry['publicationDate']
#     publication_date = publication_date.split('/')
#     for i, n in enumerate(publication_date):
#         publication_date[i] = int(n)
#     year = publication_date[2]
#     day = publication_date[1]
#     if day < 10:
#         day = f'0{day}'
#     month = publication_date[0]    
#     if month < 10:
#         month = f'0{month}'
#     publication_date = f'{year}-{month}-{day}'

#     # marketCountry
#     marketCountry = entry['marketCountry']

#     # Nutrients
#     nutrient_list = []
#     for nutriententry in entry['foodNutrients']:
#         element = ""
#         nutrient_name = nutriententry['nutrient']['name']
#         id = str(nutriententry['nutrient']['id'])
#         amount = str(nutriententry['amount'])
#         unitname = nutriententry['nutrient']['unitName']
#         if unitname == "Âµg":
#             unitname = 'ug'
#         element = f'{nutrient_name} ({id}): {amount}{unitname}'
#         nutrient_list.append(element)
#     nutrient_list.sort()
    
#     # Ingredients
#     ingredients = entry['ingredients']
#     Branded.objects.create(
#         brandOwner=brandOwner,
#         name=name,
#         fdc_id=fdc_id,
#         category=food_category,
#         publication_date=publication_date,
#         marketCountry=marketCountry,
#         nutrients=nutrient_list,
#         ingredients=ingredients
#     )
#     count += 1
#     print(f'Finished Branded: {count}')
