from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone
from django.template.defaulttags import register
from foods.models import FoodHistory, Food
from .nutritional_goals import DailyNutrients
from accounts.models import Users

import ast
import string
import datetime
from statistics import mean


# Create your views here.
class ProfileView(View):
    template_name = 'profile.html'
    model = FoodHistory
    current_user = Users

    macro_goal = {}
    today_total = {}
    today_total_2 = {}
    today_goal = {}
    units = {}

    def get(self, request):
        try:
            return render(request, 'profile.html', {'daily_goal': self.daily_goal(),
                                                    'today_total': self.today_total_2,
                                                    'date': self.current_date(),
                                                    'goal': self.macro_goal})
        except TypeError:
            return render(request, 'profile.html', {'daily_goal': 'No foods logged today.'})

    def update_history(self):
        qs = self.model.objects.filter(username=self.request.user.username).values('food_id', 'date')
        food_ids = [item['food_id'] for item in qs if item['date'].day == timezone.now().day]
        nutrients = []
        for id in food_ids:
            nutrients.append(Food.objects.filter(id=id).values('nutrients')[0]['nutrients'])
        return nutrients

    def get_age_sex(self):
        qs = self.current_user.objects.filter(
            username=self.request.user.username).values('age', "sex", 'id')
        return qs

    def current_date(self):
        d = datetime.date.today()
        d = d.strftime('%a, %b %d')
        return d

    def daily_goal(self):
        # Get history
        history = self.update_history()
        # print(f'history = {history}\n')
        # Get age and sex
        age_sex = self.get_age_sex()
        # print(age_sex[0]['id'])
        # print(f'age_sex = {age_sex}\n')
        age = int(age_sex[0]['age'])
        sex = age_sex[0]['sex']
        # Get nutrient weight totals from history
        nutrient_balance = {}  # {nutrient_name: amount}
        for nutrient_list in history:
            nutrient_list = ast.literal_eval(nutrient_list)  # convert to actual list
            for nutrient in nutrient_list:
                nutrient = nutrient.split(": ")  # [nutrient_name, amount]
                # Get int value
                for i, char in enumerate(nutrient[1]):
                    if char in string.digits:
                        nutrient_amount = float(nutrient[1][:i + 1])
                # Add to balance
                if nutrient_balance.get(nutrient[0]):
                    nutrient_balance[nutrient[0]] += nutrient_amount
                else:
                    nutrient_balance[nutrient[0]] = nutrient_amount
        # Get appropriate nutritional goals based age and sex
        nutritional_goal = DailyNutrients(age, sex)
        goal = nutritional_goal.get_daily_nutrition()
        goal_dict = {}
        percentages = {}
        # Create dictionary to for simpler iteration
        for category in [*goal][1:]:
            for goal_nutrient in [*goal[category]]:
                if type(goal[category][goal_nutrient]) != type(str()):
                    goal_nutrient_key = goal_nutrient.split(" (")
                    goal_dict[goal_nutrient_key[0]] = goal[category][goal_nutrient]
                    self.units[goal_nutrient_key[0]] = goal_nutrient_key[1].replace(')', '')
                else:
                    goal_nutrient_key = goal_nutrient.split(" (")
                    if goal_nutrient_key[0] == 'Total lipid':
                        avg = [eval(z) for z in goal[category][goal_nutrient].split('-')]
                        goal_dict[goal_nutrient_key[0]] = (avg[0] + avg[1]) / 2
                        self.units[goal_nutrient_key[0]] = goal_nutrient_key[1].replace(')', '')
        # Calculate percentages
        for goal_nutrient in [*goal_dict]:
            for nutrient in [*nutrient_balance]:
                if goal_nutrient in nutrient:
                    percentages[goal_nutrient] = round(
                        nutrient_balance[nutrient] / goal_dict[goal_nutrient], 2) * 100
        overages = {}
        deficits = {}
        percent_sum = 0
        """
        Get sum while excluding excess nutrition, and noting which nutrients
        are in excess (overages), which are not (deficits), and their amounts.
        """
        for nutrient in [*percentages]:
            if percentages[nutrient] >= 100:
                overages[nutrient] = percentages[nutrient]
                percent_sum += 100  # Excludes excess percentage
            else:
                deficits[nutrient] = percentages[nutrient]
                percent_sum += percentages[nutrient]

        self.today_goal = goal_dict
        important_ = ['Protein', 'Carbohydrate, by difference', 'Total lipid (fat)']
        for k1, v1 in nutrient_balance.items():
            if any(x == k1 for x in important_):
                if k1.startswith('Carbohydrate'):
                    self.today_total['Carbohydrate'] = round(v1)
                elif k1.startswith('Total'):
                    self.today_total['Total lipid'] = round(v1)
                else:
                    self.today_total[k1] = round(v1)

        print(self.today_goal)
        for k, v in self.today_goal.items():
            self.macro_goal[k] = f'{v}{self.units[k]}'
        print(self.macro_goal)
        for k1, v1 in self.today_total.items():
            self.today_total_2[k1] = f'{v1}{self.units[k1]}'
        # print(f'goal_dict = {goal_dict}\n')
        # print(f'nutrient_balance = {nutrient_balance}\n')
        # print(f'percentages = {percentages}\n')
        # print(f'overages: {overages}')
        # print(f'deficits: {deficits}')
        # print(f'You are exceeding your daily reccommended amounts of:')
        # for nutrient in [*overages]:
        #     print(f'{nutrient} by {(overages[nutrient]-100)}%')
        # # print('\n')
        # print(f'You are under your daily reccommended amounts of:')
        # for nutrient in [*deficits]:
        #     print(f'{nutrient} by {(100-deficits[nutrient])}%')
        percent_sum = percent_sum / len(percentages)  # fix division by zero error if no foods logged
        percent_sum = f'{percent_sum:.2f}'  # Includes zero at the end
        return percent_sum


@register.filter
def lookup(dictionary, key):
    return dictionary.get(key)
