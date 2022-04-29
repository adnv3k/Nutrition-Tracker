import requests

from django.db.models import Q
from django.views.generic import TemplateView, ListView

from .models import Food
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
            compare = {"total_entries": 0, "total_energy": 0, "total_carbs": 0}
            skip = ["Nong Shim Co., Ltd.", "Nasoya Foods USA, LLC", "United Natural Foods, Inc."]
            # print(json)
            # print(len(json))
            # f = shelve.open[3]
            end_search = ep().end_search(api_key=usda_key, query=query)
            params = end_search[1]
            url = end_search[0]
            food_query = requests.get(url, params=params)
            food_dict = {}  # add foods and their respective nutrients to dict
            nutrients_list = []
            for food in food_query.json():
                nutrients_unformat = food['foodNutrients']
                nutrients_clean = []
                name = [value['name'] for value in nutrients_unformat]
                amount = [value['amount'] for value in nutrients_unformat]
                unit = [value['unitName'] for value in nutrients_unformat]
                for name, amount, unit in zip(name, amount, unit):
                    nutrients_clean.append("".join(f"{name}: {amount}{unit}"))
                nutrients_list.append(nutrients_clean)
                food_dict['food'] = {'description': food['description'], 'foodNutrients': food['foodNutrients']}

                Food.objects.get_or_create(name=food_dict['food']['description'], nutrients=nutrients_list)

            return Food.objects.filter(Q(name__icontains=[query])).first()
