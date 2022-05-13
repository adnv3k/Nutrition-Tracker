import requests
import time

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension

from .models import Food, FoodHistory
from .endpoints import Endpoints as ep
from .api import usda_key


class HomePageView(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):
    model = Food
    template_name = 'search_results.html'
    paginate_by = 15

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
            Food.objects.get_or_create(
                name=food['description'], nutrients=nutrients_clean, dataType=params['dataType'])
        p = Paginator(Food.objects.all().filter(Q(name__icontains=[query])), 15)
        page_num = self.request.GET.get('page')
        page_obj = p.get_page(page_num)
        return render(self.request, 'search_results.html', {'page_obj': page_obj})

    def get_queryset(self):
        q = self.request.GET.get("q")
        if self.request.GET.get("brand"):
            dataType = 'Branded'
        else:
            dataType = 'SR Legacy'

        vector = SearchVector("name", "dataType")
        query = SearchQuery(q) & SearchQuery(dataType)
        food_q = Food.objects.annotate(
            rank=SearchRank(vector, query), search=vector).filter(search=query).order_by('-rank')
        if food_q.exists():
            return food_q
        else:
            return self.search(q, dataType)


def add_food(request):
    if request.method == "POST":
        if request.POST.get('addBtn'):
            if request.user.is_authenticated:
                items = dict(request.POST.items())
                food_id = int(Food.objects.filter(name=items['addBtn']).values('id')[0]['id'])
                FoodHistory.objects.get_or_create(username=items['username'],
                                                 food=items['addBtn'],
                                                 date=timezone.now(),
                                                 food_id=food_id)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect('../login')
