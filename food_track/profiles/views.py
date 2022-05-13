from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone
from foods.models import FoodHistory, Food
from .nutritional_goals import DailyNutrients
from accounts.models import Users

import ast
import string

# TODO make daily_goal shorter
# TODO account for different units when finding percentages

# Create your views here.
class ProfileView(View):
    template_name = 'profile.html'
    model = FoodHistory
    current_user = Users

    def get(self, request):
        try:
            return render(request, 'profile.html', {'daily_goal': self.daily_goal()})
        except TypeError:
            return render(request, 'profile.html', {'daily_goal': 'No foods logged today.'})

    def update_history(self):
        qs = self.model.objects.filter(username=self.request.user.username).values('food_id', 'date')
        days = [item['date'] for item in qs]
        for day in days:
            if day.day != timezone.now().day:
                pass
            else:
                food_ids = [item['food_id'] for item in qs]
                nutrients = []
                for id in food_ids:
                    nutrients.append(Food.objects.filter(id=id).values('nutrients')[0]['nutrients'])
                return nutrients

    def get_age_sex(self):
        qs = self.current_user.objects.filter(
            username=self.request.user.username).values('age', "sex", 'id')
        return qs

    def daily_goal(self):
        # Get history
        history = self.update_history()
        print(f'history = {history}\n')
        # Get age and sex
        age_sex = self.get_age_sex()
        print(f'id: {age_sex[0]["id"]}')
        print(f'age_sex = {age_sex}\n')
        age = int(age_sex[0]['age'])
        sex = age_sex[0]['sex']
        # Get nutrient weight totals from history
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
        # Get appropriate nutritional goals based age and sex           
        nutritional_goal = DailyNutrients(age, sex)
        goal = nutritional_goal.get_daily_nutrition()
        # Create dictionary to for simpler iteration
        goal_dict = {} # {'nutrient': value}
        for category in [*goal][1:]:
            for goal_nutrient in [*goal[category]]:
                if type(goal[category][goal_nutrient]) != type(str()):
                    goal_nutrient_key = goal_nutrient.split(" (")
                    goal_dict[goal_nutrient_key[0]] = goal[category][goal_nutrient]
        goal_names_bank = nutritional_goal.get_goal_names_bank()

        balance_copy = nutrient_balance.copy()
        # delete
        for goal_nutrient in [*goal_names_bank]:
            for variant in goal_names_bank[goal_nutrient]:
                if variant in [*balance_copy]:
                    del balance_copy[variant]

        sortlist = [*balance_copy]
        sortlist.sort()
        sortedbalance = {}
        for name in sortlist:
            sortedbalance[name] = balance_copy[name]

        print(f'BALANCE_COPY: {sortedbalance}\n')
        sorted_nutrient_balance = {}
        names_list = [*nutrient_balance]
        names_list.sort()
        for name in names_list:
            sorted_nutrient_balance[name] = nutrient_balance[name]
        nutrient_names_bank = nutritional_goal.get_nutrient_names_bank()
        print(f'{nutrient_names_bank}\n')


        # Intermediary
        intermediary = {}
        # goal_names_bank = nutritional_goal.get_goal_names_bank()
        for goal_nutrient in [*goal_dict]:
            intermediary[goal_nutrient] = 0
            for variant in goal_names_bank[goal_nutrient]:
                if nutrient_balance.get(variant):
                    intermediary[goal_nutrient] += nutrient_balance[variant]
        print(f'intermediary = {intermediary}\n')

        adequate_intakes = ["Chromium", "Fluoride", "Manganese", "Potassium",
                            "Sodium", "Chloride", "Pantothenic Acid", "Biotin", "Iodine", "Molybdenum"]
        # Calculate percentages
        percentages = {}
        for goal_nutrient in [*goal_dict]:
            for intermediate in intermediary:
                if goal_nutrient in intermediate:
                    # does not handle 'nutrient, other stuff' nutrient names well
                    if goal_nutrient in adequate_intakes:
                        continue
                    # Handle units
                    elif "Copper" in goal_nutrient:
                        percentages[goal_nutrient] = round(
                        intermediary[intermediate] / (goal_dict[goal_nutrient]/1000), 2) * 100
                    elif "Water" in goal_nutrient:
                        percentages[goal_nutrient] = round(
                        intermediary[intermediate] / (goal_dict[goal_nutrient]*1000), 2) * 100

                    else:
                        percentages[goal_nutrient] = round(
                        intermediary[intermediate] / goal_dict[goal_nutrient], 2) * 100

        overages = {}
        deficits = {}
        percent_sum = 0
        """
        Get sum while excluding excess nutrition, and noting which nutrients
        are in excess (overages), which are not (deficits), and their amounts.
        """
        for nutrient in [*percentages]:
            if percentages[nutrient] >= 100:
                percent_sum += 100 # Exclude excess percentage
                overages[nutrient] = percentages[nutrient] # Save excess
            else:
                percent_sum += percentages[nutrient]
                deficits[nutrient] = percentages[nutrient] # Save deficit
        print(f'goal_dict = {goal_dict}\n')


        print(f'goal_names_bank = {goal_names_bank}\n')
        print(f'nutrient_balance = {sorted_nutrient_balance}\n')
        # print(f'nutrient_balance = {nutrient_balance}\n')
        print(f'percentages = {percentages}\n')
        print(f'overages: {overages}\n')
        print(f'deficits: {deficits}\n')
        print(f'You are exceeding your daily reccommended amounts of:')
        for nutrient in [*overages]:
            print(f'{nutrient} by {(overages[nutrient]-100)}%')
        print('\n')
        print(f'You are under your daily reccommended amounts of:')
        for nutrient in [*deficits]:
            print(f'{nutrient} by {(100-deficits[nutrient])}%')
        percent_sum = percent_sum / len(percentages) 
        percent_sum = f'{percent_sum:.2f}' # Includes zero at the end
        return percent_sum
        