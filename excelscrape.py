"""Input: Sex and Age
Output: daily dietary recommendation
"""
import os
from re import split
import sys
from openpyxl.worksheet import worksheet
import requests
import shelve
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

os.chdir(r'.\\USDA')

# Reading excel
# workbook = pd.read_excel('Daily Nutritional Goals.xlsx')
# print(workbook.head(15))

# workbook = openpyxl.load_workbook("Daily Nutritional Goals.xlsx")
# sheet = workbook.copy_worksheet(workbook.worksheets[0])
# print(type(sheet))
# print(sheet.columns)

# print(workbook.sheetnames)
# print(sheet['A4'])
# cell = sheet['C2']
# print(type(cell.value))
# print(cell.value)

# sheet.cell(row=1, column=2)
# sheet.cell(row=1, column=2).value

# To grab the nutrientnames
# macronutrients = []
# for i in range(5,15):
#     macronutrients.append(str(sheet.cell(row=i,column=1).value))
# # print(macronutrients)

# minerals = []
# for i in range(16,23):
#     minerals.append(str(sheet.cell(row=i,column=1).value))
# # print(minerals)

# vitamins = []
# for i in range(24,36):
#     vitamins.append(str(sheet.cell(row=i,column=1).value))
# # print(vitamins)

# Save nutrient names
# daily = {"macronutrients": macronutrients, "minerals": minerals, "vitamins": vitamins}
# os.chdir(r'..\\')
# file = shelve.open('usda')
# file['daily_nutrition'] = daily
# file.close()

# Associate nutrient names with a value
# print(sheet.cell(row=2,column=13).value)
# column = 3

# test = sheet.cell(row=2,column=column).value
# print(f'Sex: {test[0]}')
# for ele in test:
#     print(ele)
# print(len(test))
# test = test.split('\n')
# print(test)
# age_range = test[1].split('-')
# print(age_range)
# f=shelve.open[3]

"""The idea is to input ur sex and age, then it will pull up the appropriate daily nutrition.
Save every group (sex,agerange) 
daily
    sex
        age
input: sex = Female
daily['F']
input: age = 26
daily['F']
for key in [*daily['F']]:
    if age <= upper_age_range:
        load this group
"""
#extract from the excel
# daily = {"F": {}, "M": {}}
# for column in range(3,16):

#     calories = {'Calories': sheet.cell(row=3,column=column).value}
#     # print(calories)

#     macronutrients = {}
#     for i in range(5,15):
#         macronutrients[str(sheet.cell(row=i,column=1).value)] = sheet.cell(row=i,column=column).value
#     # print(macronutrients)

#     minerals = {}
#     for i in range(16,23):
#         minerals[str(sheet.cell(row=i,column=1).value)] = sheet.cell(row=i,column=column).value
#     # print(minerals)

#     vitamins = {}
#     for i in range(24,36):
#         vitamins[str(sheet.cell(row=i,column=1).value)] = sheet.cell(row=i,column=column).value
#     # print(vitamins)

#     values = {"calories": calories, "macronutrients": macronutrients, "minerals": minerals, "vitamins": vitamins}

#     group = sheet.cell(row=2,column=column).value.split('\n')
#     if group[0] == "M/F":
#         upper_range = int(group[1].split('-')[-1])
#         lower_range = int(group[1].split('-')[0])
#         daily['F'][(lower_range,upper_range)] = values
#         daily['M'][(lower_range,upper_range)] = values
#         continue
#     if "+" in group[1]:
#         upper_range = 130
#         lower_range = 51
#     else:
#         upper_range = int(group[1].split('-')[-1])
#         lower_range = int(group[1].split('-')[0])
#     daily[group[0]][(lower_range,upper_range)] = values

# print(daily)

# Save
# os.chdir(r'..\\')
# file = shelve.open('usda')
# file['daily_nutrition'] = daily
# file.close()
#
# Open
os.chdir(r'..\\')
file = shelve.open('usda')
daily = file['daily_nutrition']
file.close()


# Getting daily rec for age and sex
age = 35
sex = "M"
for age_range in [*daily[sex]]:
    if age in range(age_range[0],age_range[1]+1):
        daily_nutrition = daily[sex][age_range]
        print(daily[sex][age_range])


# 1 IU retinol = 0.3 mcg RAE
# 18:2 lineoic acid 
# PUFA 18:2 n-6 c,c
# PUFA 18:2
# Fatty acids, total polyunsaturated

# 18:3 lineoic acid 
# PUFA 18:3 n-3 c,c,c (ALA)
# PUFA 18:3
# Fatty acids, total polyunsaturated