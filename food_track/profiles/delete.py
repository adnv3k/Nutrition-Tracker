from nutritional_goals import DailyNutrients

import json
import string
import ast

daily = DailyNutrients()
goal = daily.get_daily_nutrition(30, "M")

nutrients = [
    "['Protein: 10.6G', 'Total lipid (fat): 12.9G', 'Carbohydrate, by difference: 35.3G', 'Energy: 306KCAL', 'Sugars, total including NLEA: 4.71G', 'Fiber, total dietary: 1.2G', 'Calcium, Ca: 176MG', 'Iron, Fe: 1.69MG', 'Sodium, Na: 847MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 29.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 5.29G']",
    "['Protein: 7.89G', 'Total lipid (fat): 0.0G', 'Carbohydrate, by difference: 55.3G', 'Energy: 263KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 2.6G', 'Calcium, Ca: 0.0MG', 'Iron, Fe: 0.95MG', 'Sodium, Na: 553MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 0.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 0.0G']",
    "['Protein: 21.4G', 'Total lipid (fat): 25.0G', 'Carbohydrate, by difference: 0.0G', 'Energy: 346KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 0.0G', 'Calcium, Ca: 714MG', 'Iron, Fe: 0.0MG', 'Sodium, Na: 536MG', 'Vitamin A, IU: 714IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 146MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 14.3G']",
        "['Protein: 10.6G', 'Total lipid (fat): 12.9G', 'Carbohydrate, by difference: 35.3G', 'Energy: 306KCAL', 'Sugars, total including NLEA: 4.71G', 'Fiber, total dietary: 1.2G', 'Calcium, Ca: 176MG', 'Iron, Fe: 1.69MG', 'Sodium, Na: 847MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 29.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 5.29G']",
    "['Protein: 7.89G', 'Total lipid (fat): 0.0G', 'Carbohydrate, by difference: 55.3G', 'Energy: 263KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 2.6G', 'Calcium, Ca: 0.0MG', 'Iron, Fe: 0.95MG', 'Sodium, Na: 553MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 0.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 0.0G']",
    "['Protein: 21.4G', 'Total lipid (fat): 25.0G', 'Carbohydrate, by difference: 0.0G', 'Energy: 346KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 0.0G', 'Calcium, Ca: 714MG', 'Iron, Fe: 0.0MG', 'Sodium, Na: 536MG', 'Vitamin A, IU: 714IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 146MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 14.3G']",    "['Protein: 10.6G', 'Total lipid (fat): 12.9G', 'Carbohydrate, by difference: 35.3G', 'Energy: 306KCAL', 'Sugars, total including NLEA: 4.71G', 'Fiber, total dietary: 1.2G', 'Calcium, Ca: 176MG', 'Iron, Fe: 1.69MG', 'Sodium, Na: 847MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 29.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 5.29G']",
    "['Protein: 7.89G', 'Total lipid (fat): 0.0G', 'Carbohydrate, by difference: 55.3G', 'Energy: 263KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 2.6G', 'Calcium, Ca: 0.0MG', 'Iron, Fe: 0.95MG', 'Sodium, Na: 553MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 0.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 0.0G']",
    "['Protein: 21.4G', 'Total lipid (fat): 25.0G', 'Carbohydrate, by difference: 0.0G', 'Energy: 346KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 0.0G', 'Calcium, Ca: 714MG', 'Iron, Fe: 0.0MG', 'Sodium, Na: 536MG', 'Vitamin A, IU: 714IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 146MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 14.3G']",    "['Protein: 10.6G', 'Total lipid (fat): 12.9G', 'Carbohydrate, by difference: 35.3G', 'Energy: 306KCAL', 'Sugars, total including NLEA: 4.71G', 'Fiber, total dietary: 1.2G', 'Calcium, Ca: 176MG', 'Iron, Fe: 1.69MG', 'Sodium, Na: 847MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 29.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 5.29G']",
    "['Protein: 7.89G', 'Total lipid (fat): 0.0G', 'Carbohydrate, by difference: 55.3G', 'Energy: 263KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 2.6G', 'Calcium, Ca: 0.0MG', 'Iron, Fe: 0.95MG', 'Sodium, Na: 553MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 0.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 0.0G']",
    "['Protein: 21.4G', 'Total lipid (fat): 25.0G', 'Carbohydrate, by difference: 0.0G', 'Energy: 346KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 0.0G', 'Calcium, Ca: 714MG', 'Iron, Fe: 0.0MG', 'Sodium, Na: 536MG', 'Vitamin A, IU: 714IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 146MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 14.3G']","['Protein: 10.6G', 'Total lipid (fat): 12.9G', 'Carbohydrate, by difference: 35.3G', 'Energy: 306KCAL', 'Sugars, total including NLEA: 4.71G', 'Fiber, total dietary: 1.2G', 'Calcium, Ca: 176MG', 'Iron, Fe: 1.69MG', 'Sodium, Na: 847MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 29.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 5.29G']",
    "['Protein: 7.89G', 'Total lipid (fat): 0.0G', 'Carbohydrate, by difference: 55.3G', 'Energy: 263KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 2.6G', 'Calcium, Ca: 0.0MG', 'Iron, Fe: 0.95MG', 'Sodium, Na: 553MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 0.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 0.0G']",
    "['Protein: 21.4G', 'Total lipid (fat): 25.0G', 'Carbohydrate, by difference: 0.0G', 'Energy: 346KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 0.0G', 'Calcium, Ca: 714MG', 'Iron, Fe: 0.0MG', 'Sodium, Na: 536MG', 'Vitamin A, IU: 714IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 146MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 14.3G']",
    "['Protein: 10.4G', 'Total lipid (fat): 20.8G', 'Carbohydrate, by difference: 44.8G', 'Energy: 408KCAL', 'Alcohol, ethyl: 0.0G', 'Water: 21.1G', 'Caffeine: 0.0MG', 'Theobromine: 0.0MG', 'Sugars, total including NLEA: 2.08G', 'Fiber, total dietary: 2.1G', 'Calcium, Ca: 90.0MG', 'Iron, Fe: 2.49MG', 'Magnesium, Mg: 17.0MG', 'Phosphorus, P: 120MG', 'Potassium, K: 84.0MG', 'Sodium, Na: 750MG', 'Zinc, Zn: 0.96MG', 'Copper, Cu: 0.086MG', 'Selenium, Se: 19.8UG', 'Retinol: 23.0UG', 'Vitamin A, RAE: 24.0UG', 'Carotene, beta: 9.0UG', 'Carotene, alpha: 1.0UG', 'Vitamin E (alpha-tocopherol): 1.49MG', 'Vitamin D (D2 + D3): 0.1UG', 'Cryptoxanthin, beta: 0.0UG', 'Lycopene: 0.0UG', 'Lutein + zeaxanthin: 45.0UG', 'Vitamin C, total ascorbic acid: 0.0MG', 'Thiamin: 0.433MG', 'Riboflavin: 0.303MG', 'Niacin: 3.28MG', 'Vitamin B-6: 0.048MG', 'Folate, total: 107UG', 'Vitamin B-12: 0.24UG', 'Choline, total: 8.5MG', 'Vitamin K (phylloquinone): 32.4UG', 'Folic acid: 75.0UG', 'Folate, food: 32.0UG', 'Folate, DFE: 159UG', 'Vitamin E, added: 0.0MG', 'Vitamin B-12, added: 0.0UG', 'Cholesterol: 10.0MG', 'Fatty acids, total saturated: 6.25G', 'SFA 4:0: 0.153G', 'SFA 6:0: 0.073G', 'SFA 8:0: 0.043G', 'SFA 10:0: 0.096G', 'SFA 12:0: 0.111G', 'SFA 14:0: 0.401G', 'SFA 16:0: 3.62G', 'SFA 18:0: 1.48G', 'MUFA 18:1: 4.17G', 'PUFA 18:2: 8.1G', 'PUFA 18:3: 1.1G', 'PUFA 20:4: 0.0G', 'PUFA 22:6 n-3 (DHA): 0.0G', 'MUFA 16:1: 0.076G', 'PUFA 18:4: 0.0G', 'MUFA 20:1: 0.039G', 'PUFA 2:5 n-3 (EPA): 0.0G', 'MUFA 22:1: 0.0G', 'PUFA 22:5 n-3 (DPA): 0.0G', 'Fatty acids, total monounsaturated: 4.34G', 'Fatty acids, total polyunsaturated: 9.2G']"
]
nutrient_balance = {}
for nutrient_list in nutrients:
    nutrient_list = ast.literal_eval(nutrient_list)  # convert to actual list
    for nutrient in nutrient_list:
        nutrient = nutrient.split(": ")  # [nutrient, amount]
        # Get int value
        for i, char in enumerate(nutrient[1]):
            if char not in string.ascii_uppercase:
                nutrient_amount = float(nutrient[1][:i+1])
        # Add to balance
        if nutrient_balance.get(nutrient[0]):
            nutrient_balance[nutrient[0]] += nutrient_amount
        else:
            nutrient_balance[nutrient[0]] = nutrient_amount
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
# print(percentages)
# print(len(percentages))
total_percent = sum(list(percentages.values()))/len(percentages)
# print(total_percent)
# print(nutrient_balance)