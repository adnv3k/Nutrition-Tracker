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
        nutrient_balance = {} # {nutrient_name: amount}
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
        goal_dict = {}
        percentages = {}
        for category in [*goal][1:]:
            for goal_nutrient in [*goal[category]]:
                if type(goal[category][goal_nutrient]) != type(str()):
                    goal_nutrient_key = goal_nutrient.split(" (")
                    goal_dict[goal_nutrient_key[0]] = goal[category][goal_nutrient]
        for goal_nutrient in [*goal_dict]:
            for nutrient in [*nutrient_balance]:
                if goal_nutrient in nutrient:
                    percentages[goal_nutrient] = nutrient_balance[nutrient]/goal_dict[goal_nutrient]
                    if percentages[goal_nutrient] > 1:
                        percentages[goal_nutrient] = 1
        total_percent = sum(list(percentages.values()))/len(percentages)*100



        return total_percent
        