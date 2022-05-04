from django.shortcuts import render, HttpResponse
from django.views.generic import View
from foods.models import FoodHistory
from .nutritional_goals import DailyNutrients

import ast
import string

# Create your views here.
class ProfileView(View):
    template_name = 'profile.html'
    model = FoodHistory

    def get(self, request):
        return render(request, 'profile.html', {'daily_goal': self.daily_goal()})

    def update_history(self):
        qs = self.model.objects.filter(username=self.request.user.username).values('nutrients')
        return qs

    def daily_goal(self):
        history = self.update_history()
        history = [item['nutrients'] for item in history]
        nutrient_balance = {}
        for nutrient_list in history:
            nutrient_list = ast.literal_eval(nutrient_list) # convert to actual list
            for nutrient in nutrient_list:
                nutrient = nutrient.split(": ") # [nutrient_name, amount]
                # Get int value
                for i, char in enumerate(nutrient[1]):
                    if char in string.digits:
                        nutrient_amount = float(nutrient[1][:i+1])
                # Add to balance
                if nutrient_balance.get(nutrient[0]):
                    nutrient_balance[nutrient[0]] += nutrient_amount
                else:
                    nutrient_balance[nutrient[0]] = nutrient_amount
        nutritional_goal = DailyNutrients()
        goal = nutritional_goal.get_daily_nutrition(30, "M")
        print(nutrient_balance)
        


        return 43
        


