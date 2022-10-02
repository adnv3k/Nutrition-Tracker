from genericpath import exists
from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone
from sqlalchemy import false, true
from foods.models import Branded, FoodHistory, Food, SRLegacy
from .nutritional_goals import DailyNutrients
from accounts.models import Users

import ast
import string


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
        qs = self.model.objects.filter(username=self.request.user.username).values('fdc_id', 'date')
        days = [item['date'] for item in qs]
        for day in days:
            if day.day != timezone.now().day:
                pass
            else:
                food_ids = [item['fdc_id'] for item in qs]
                nutrients = []
                for id in food_ids:
                    try:
                        nutrients.append(SRLegacy.objects.filter(fdc_id=id).values('nutrients')[0]['nutrients'])
                    except:
                        nutrients.append(Branded.objects.filter(fdc_id=id).values('nutrients')[0]['nutrients'])
                return nutrients

    def get_age_sex(self):
        qs = self.current_user.objects.filter(
            username=self.request.user.username).values('age', "sex", 'id')
        return qs

    def daily_goal(self):
        # Get history
        history = self.update_history()
        print(f'history =\n')
        for food in history:
            print(food)
        # Get age and sex
        age_sex = self.get_age_sex()
        print(age_sex[0]['id'])
        print(f'age_sex = {age_sex}\n')
        age = int(age_sex[0]['age'])
        sex = age_sex[0]['sex']
        # Get nutrient weight totals from history
        nutrient_balance = {} # {nutrient_name: amount}
        #TODO add in calc by serving size in grams
        for nutrient_list in history:
            vit_d_added = False
            vit_a_added = False
            folate_added = False
            nutrient_list = ast.literal_eval(nutrient_list) # convert to actual list
            for nutrient in nutrient_list:
                nutrient_name, nutrient_amount = get_name_amount(nutrient)

                # Vitamin D
                if "n D" in nutrient_name:
                    if vit_d_added:
                        continue
                    vit_d_added = True
                    int_found = False
                    for searchnutrient in nutrient_list:
                        if "International" in searchnutrient:
                            int_found = True
                            nutrient_name, nutrient_amount = get_name_amount(searchnutrient)
                            print(f'found Vit D IU\n')
                            break
                    if not int_found:
                        # print(f'nutrientname: {nutrient[0]} nutrient_amount: {nutrient_amount}\n')
                        nutrient_amount /= 0.025
                        nutrient_name = "Vitamin D (D2 + D3), International Units (1110)"
                        # print(f'nutrientname: {nutrient[0]} nutrient_amount: {nutrient_amount}\n')
               
                # Vitamin A
                elif "n A" in nutrient_name or "Carotene" in nutrient_name:
                    print(f'vitamin A name: {nutrient_name}\n')
                    if vit_a_added:
                        continue
                    vit_a_added = True
                    rae_found = False
                    other = []
                    for searchnutrient in nutrient_list:
                        nutrient_name, nutrient_amount = get_name_amount(searchnutrient)
                        if "RAE" in searchnutrient:
                            rae_found = True
                            print(f'found rae {nutrient_name}. nutrient_amount: {nutrient_amount}\n')
                            break
                        if "Retinol" in nutrient_name:
                            other.append([nutrient_name, nutrient_amount])
                        elif "Carotene" in nutrient_name:
                            if "alpha" in nutrient_name:
                                nutrient_amount /= 24
                            else:
                                nutrient_amount /= 12
                            other.append([nutrient_name, nutrient_amount])
                        elif "Cryptoxanthin" in nutrient_name:
                            other.append([nutrient_name, nutrient_amount / 24])
                        elif "A, IU" in nutrient_name:
                            other.insert(0, [nutrient_name, nutrient_amount])
                    if not rae_found:
                        print(f'rae not found')
                        nutrient_amount = 0
                        if "A, IU" in other[0][0]:
                            nutrient_amount = other[0][1] * 0.3000
                            print('iu found\n')
                        else:
                            for ele in other:
                                nutrient_amount += ele[1]
                        nutrient_name = "Vitamin A, RAE (1106)"
                        print(f'amount: {nutrient_amount}\n')

                # Vitamin E
                elif "Vitamin E" in nutrient_name:
                    print(f'found vitamin e: {nutrient_name}\n')
                    nutrient_name = "Vitamin E (alpha-tocopherol) (1109)"
                # Vit B
                elif "B-12" in nutrient_name:
                    print(f'found vit b: {nutrient_name}\n')
                    nutrient_name = "Vitamin B-12 (1178)"
                # Niacin
                elif "Tryptophan" in nutrient_name:
                    print(f'found tryptophan: {nutrient_name} ')
                    nutrient_name = "Niacin (1167)"
                    nutrient_amount = nutrient_amount * 1000 / 60
                    print(f'nutrient_amount: {nutrient_amount}\n')
                elif "Vitamin K" in nutrient_name:
                    nutrient_name = "Vitamin K"
                # Folate
                elif "Folate" in nutrient_name:
                    if folate_added:
                        continue
                    folate_added = True
                    dfe_found = False
                    other = []
                    for searchnutrient in nutrient_list:
                        if "Folate, DFE" in searchnutrient:
                            print(f'dfe found.')
                            nutrient_name, nutrient_amount = get_name_amount(searchnutrient)
                            print(f'nutrient_amount: {nutrient_amount}\n')
                            dfe_found = True
                            break
                        elif "Folic acid" in searchnutrient:
                            nutrient_name, nutrient_amount = get_name_amount(searchnutrient)
                            other.append([nutrient_name, nutrient_amount * 1.7000])
                        elif "Folate" in searchnutrient:
                            nutrient_name, nutrient_amount = get_name_amount(searchnutrient)
                            other.append([nutrient_name, nutrient_amount])
                            print(f'folate, food found. other: {other}\n')
                    if not dfe_found:
                        nutrient_amount = 0
                        for ele in other:
                            nutrient_amount += ele[1]
                            if nutrient_amount / 2 == ele[1]:
                                print(f'folate food == total\n')
                                nutrient_amount /= 2
                        nutrient_name = "Folate, DFE (1190)"
                        print(f'dfe not found. dfe calculated: {nutrient_amount}\n')
                # Add to balance
                if nutrient_balance.get(nutrient_name):
                    nutrient_balance[nutrient_name] += nutrient_amount
                else:
                    nutrient_balance[nutrient_name] = nutrient_amount
                # if vit_d_added:
                #     print(f'{nutrient[0]} added: {nutrient_amount}\nbalance:{nutrient_balance[nutrient[0]]}')
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
        # Calculate percentages
        for goal_nutrient in [*goal_dict]:
            for nutrient in [*nutrient_balance]:
                if goal_nutrient in nutrient:
                    for nut in ["n D", "n A", "n E", "Folate", "Vitamin K"]:
                        if nut in goal_nutrient:
                            print(f'goal_nutrient: {goal_nutrient}: {nutrient_balance[nutrient]}\n')
                            break
                    percentages[goal_nutrient] = round(
                        nutrient_balance[nutrient] / goal_dict[goal_nutrient], 5) * 100.0000
                    break
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
        print(f'goal_dict = {goal_dict}\n')
        print(f'nutrient_balance = {nutrient_balance}\n')
        print(f'percentages = {percentages}\n')
        print(f'overages: {overages}')
        print(f'deficits: {deficits}')
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
        
def get_name_amount(entry):
        nutrient = entry.split(": ")
        for i, char in enumerate(nutrient[1]):
            if char in string.digits:
                nutrient_amount = float(nutrient[1][:i+1])
        return nutrient[0], nutrient_amount