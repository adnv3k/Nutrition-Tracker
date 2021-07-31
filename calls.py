"""
Used to call the USDA class from api.py
to get various organized data.
This intended to make working with the data easier,
and is not intended to be included in final product.
"""
"""
General idea
Receive:
Profile Info
    some form of identifying information of profile
    should include sex and age
    if new profile
        save profile
    else:
        load sex and age
    load current daily nutrition balance (CDNB)
    (maybe return that info for display?)
    return some form of feedback:
        profile saved/profile loaded with CDNB

Recieve:
Food entries
    includes the food
        any filtering tags
            foundation (doesnt seem to work out too well)
            branded
            most will consult sr legacy

            if it is a brand
                search in branded database
                    rigid search parameters












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


query = 'pasta'
usda_key = '0arBG94hGw3XyzanWdsZ4I6dTCmsT1aj7QWSJkGf'
usda = USDA(usda_key)
"""SEARCH"""
usda.search(query=query)

"""EVAL"""
results = usda.get_results() # list of dictionaries
# print(results)
# file = shelve.open[d]

"""Get descriptions"""
descriptions = usda.get_descriptions()
# print(descriptions)
# print(pd.DataFrame(descriptions))
# input('enter')

"""Get nutrient names"""
# nutrient_names = usda.get_nutrient_names()
# print(nutrient_names)

"""Get nutrients"""
# nutrients = usda.get_nutrients(descriptions[1])
# print(nutrients)
# nutrients = usda.get_nutrient_names(nutrients)
# nutrients.sort()
# print(nutrients)

"""Get nutrient composition"""
# nutrient = 'Protein'
# nutrient_composition = usda.get_nutrient_composition(descriptions[1], nutrient)
# print(f'{nutrient}: {nutrient_composition}%')

"""Get nutrient names bank"""
# nutrient_names_bank = usda.get_nutrient_names_bank()
# print(nutrient_names_bank)

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

"""Get daily nutrition"""
# daily_nutrition = usda.get_daily_nutrition(age=27, sex='M')
# daily_nutrition = usda.get_daily_nutrition()

# print(daily_nutrition)
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

# nutrients_chicken = usda.get_nutrients(description=descriptions[-2])
# print(nutrients_chicken)
# print(usda.get_nutrient_names(nutrients_chicken))
# print(usda.get_unit_names_bank())

# print(usda.get_total_mass(description=descriptions[-2]))
# print(usda.convert_to_calories(nutrients_chicken[descriptions[-2]][0]['value'], nutrients_chicken[descriptions[-2]][0]['unitName']))


# df = pd.DataFrame(daily_nutrition)
# print(df.to_json())
# df = df.to_json()
# print(pd.DataFrame(df))

# Get percent comp of all nutrients given a description
# 

"""
usda_object = usda(key)


u get a usda object that u can use to
    search queries
        avocado = usda(key).search('avocado')
        avocado.get_nutrients(description) # description would be the entry description returned from search results

    retrieve nutrient names bank
    unit names bank
    daily nutrition data from table
"""

"""Get nutrient composition profile"""
# profile = usda.get_nutrient_composition_profile(descriptions[3])
# print(profile)
# df = pd.DataFrame(profile[0], columns=['Nutrient', 'Percentage'])

# print(df)
# print(
#     f'Total Percentage: {df["Percentage"].sum()}\n'
#     f'Not included %: {round(100-df["Percentage"].sum(),3)}'
#     )
def check_comp():
    percent = 0
    for nutrient in profile[0]:
        percent += nutrient[1]
    print(
        f'Total Percent: {percent}\n'
        f'Length not included list: {len(profile[1])}'
        )
# check_comp()

""" TEST check not included values"""
def test_get_nutrient_composition_profile():
    """
    checks the sum of all calculated percent composition of nutrients for every
    search result
    the closer each element in not_included is is to 0, the more accurate it is
    """
    not_included = []
    for i in range(len(descriptions)):
        profile = usda.get_nutrient_composition_profile(descriptions[i])
        df = pd.DataFrame(profile[0], columns=['Nutrient', 'Percentage'])
        percents_sum = df["Percentage"].sum()
        not_inc_percent = round(100-df["Percentage"].sum(),5)
        # if not_inc_percent > 10:
        if descriptions[i] == 'Beef, bologna, reduced asdf sodium':
            print(descriptions[i])
            # print(df)
            print(percents_sum)
            check_comp()
            s = usda.get_nutrients(descriptions[i])[descriptions[i]]
            count = []
            other = []
            otherlist = []
            for ele in profile[0]:
                other.append(ele[0])
            for nutrient in s:
                if nutrient['nutrientName'] in other:
                    otherlist.append(nutrient)
                grams = usda.convert_to_grams(nutrient['value'], nutrient['unitName'])
                if grams:
                    count.append(grams)
            # print(pd.DataFrame(s))
            # print(pd.DataFrame(otherlist))
            print(f'Total grams: {sum(count)}')
            print(f'Total mass: {usda.get_total_mass(descriptions[i])}')
            # not_in = pd.DataFrame(profile[1], columns=['Nutrient', 'Units'])
            # print(not_in)
            # print(not_in["Units"].max())
        not_included.append(not_inc_percent)
    not_included.sort()
    print(not_included)
    # print(len(not_included))
    print(sum(not_included)/len(not_included))
test_get_nutrient_composition_profile()








# Get average percent comp of every nutrient for every hit
