import requests

from django.db.models import Q
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Food, FoodHistory
from .endpoints import Endpoints as ep
from .api import usda_key


class HomePageView(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):
    model = Food
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        food_q = Food.objects.filter(Q(name__icontains=query))
        if food_q.exists():
            return food_q
        else:
            end_search = ep().end_search(api_key=usda_key, query=query)
            params = end_search[1]
            url = end_search[0]
            food_query = requests.get(url, params=params)
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
                try:
                    Food.objects.get(name=food['description'])
                except ObjectDoesNotExist:
                    Food.objects.get_or_create(name=food['description'], nutrients=nutrients_clean)
                else:
                    pass

            return Food.objects.filter(Q(name__icontains=[query])).first()


def add_food(request):
    if request.method == "POST":
        if request.POST.get('addBtn'):
            if request.user.is_authenticated:
                items = dict(request.POST.items())
                FoodHistory.objects.get_or_create(username=items['username'],
                                                  food=items['addBtn'],
                                                  nutrients=items['nutrients'],
                                                  date=timezone.now())
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("login")
