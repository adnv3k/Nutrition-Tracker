"""
Place to call the usda class to get various organized data
"""
from functools import update_wrapper
import os
import sys
from typing import Any
import requests
import shelve
import pandas as pd
import matplotlib.pyplot as plt

from api import USDA

def get_all_units():
    file = shelve.open('usda')
    units = file['unit_bank']
    file.close()
    print(f'before: {len(units)}')

    nutrients = usda.get_nutrients()
    for description in [*nutrients]:
        for nutrient in nutrients[description]:
            # print(nutrient)
            unit = nutrient['Unit']
            if unit not in units:
                units.append(unit)

    print(f'after: {len(units)}')

    file = shelve.open('usda')
    file['unit_bank'] = units
    file.close()

def save(item: Any, file_key: str, file_name:str='delete'):
    """
    item: anything
    file_key: string
    """
    file = shelve.open(file_name)
    file[file_key] = item
    file.close()
    print('Saved')

def get(file_key: str, file_name:str='delete'):
    file = shelve.open(file_name)
    item = file[file_key]
    file.close()
    return item

def process(file_key: str, item:Any=None, file_name:str='delete'):
    """
    Returns: saved datastructure at the file_key
    """
    file = shelve.open(file_name)
    if not file[file_key]:
        file.close()
        save(item=item, file_key=file_key, file_name=file_name)
    return get(file_key=file_key, file_name=file_name)


query = 'guava'
usda_key = '0arBG94hGw3XyzanWdsZ4I6dTCmsT1aj7QWSJkGf'
usda = USDA(usda_key)
"""SEARCH"""
usda.search(query=query)

"""EVAL"""
results = usda.get_results() # list of dictionaries
# print(results)
# file = shelve.open[d]

descriptions = usda.get_descriptions()
print(descriptions)
# input('enter')

# nutrient_names = usda.get_nutrient_names()
# print(nutrient_names)

# nutrients = usda.get_nutrients(descriptions[0])
# print(nutrients)

# for ele in [*nutrients]:


# nutrient_composition = usda.get_nutrient_composition(descriptions[0], 'Niacin')
# print(nutrient_composition)

# nutrient_names_bank = usda.get_nutrient_names_bank()
def check_percents(descriptions_index):
    counter = []
    # for nutrient in usda.get_nutrients(descriptions[0]):
    for nutrient in usda.get_nutrient_names_bank():
        nutrient_composition = usda.get_nutrient_composition(descriptions[descriptions_index], nutrient)
        if nutrient_composition:
            counter.append(nutrient_composition)
            # print(f'{nutrient}: {nutrient_composition}%')
    print(descriptions[descriptions_index])
    print(f'Sum of percent compositions: {round(sum(counter),3)}%\nTotal Mass: {usda.get_total_mass(descriptions[descriptions_index])}g')
# check_percents(-2)

# for i in range(10):
#     check_percents(i)
daily_nutrition = usda.get_daily_nutrition(age=27, sex='M')
# daily_nutrition = usda.get_daily_nutrition()

print(daily_nutrition)
# Processing units
# for i, nutrient_type in enumerate([*daily_nutrition]):
#     if i == 0:
#         continue
#     for name in [*daily_nutrition[nutrient_type]]:
#         split_index = name.index('(')
#         unit = name[split_index+1:-1]
#         nutrient_name = name[:split_index-1]
#         print(f'{nutrient_name} {unit}')


# print(usda.get_nutrient_names_bank())

nutrients_chicken = usda.get_nutrients(description=descriptions[-2])
# print(nutrients_chicken)
# print(usda.get_nutrient_names(nutrients_chicken))
# print(usda.get_unit_names_bank())

# print(usda.get_total_mass(description=descriptions[-2]))
# print(usda.convert_to_calories(nutrients_chicken[descriptions[-2]][0]['Value'], nutrients_chicken[descriptions[-2]][0]['Unit']))



df = pd.DataFrame(daily_nutrition)
# print(df.to_json())
df = df.to_json()
print(pd.DataFrame(df))