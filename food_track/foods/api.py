import random
import ast
import string
import json
import shelve
import pandas as pd
import requests
from .endpoints import Endpoints as ep

usda_key = '0arBG94hGw3XyzanWdsZ4I6dTCmsT1aj7QWSJkGf'

# To get pages in a range
#
# for page in range(1,51):
# url = f'https://api.nal.usda.gov/fdc/v1/foods/list?api_key={usda_key}&pageSize=200&pageNumber={page}'
# response = requests.get(url)
# json = response.json()
# print(response)
# file = shelve.open('usda_pages')
# file[str(page)] = json
# file.close()

# To get specific page
#
# page = 101
# url = f'https://api.nal.usda.gov/fdc/v1/foods/list?api_key={usda_key}&pageSize=200&pageNumber={page}'
# response = requests.get(url)
# json = response.json()
# print(response)
# file = shelve.open('usda_pages')
# file[str(page)] = json
# file.close()


# DELETE trying to get other pages
# page = 51
# query = 'chicken'
# url = f'https://api.nal.usda.gov/fdc/v1/foods/list?api_key={usda_key}&pageSize=200&pageNumber={page}&sortBy=lowercaseDescription.keyword&sortOrder=desc'
# url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={usda_key}&query={query}&pageSize=200'
# url = f'https://api.nal.usda.gov/fdc/v1/foods/list?api_key={usda_key}&pageSize=200&pageNumber={page}'

# SR Legacy datatype
# url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={usda_key}&query={query}&dataType=SR%20Legacy&pageSize=200'
# Branded datatype
# url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={usda_key}&query={query}&dataType=Branded&pageSize=200'
# Both
# url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={usda_key}&query={query}&dataType=Branded,SR%20Legacy&pageSize=200'

#
# response = requests.get(url)
# print(response.headers)
# json = response.json()
# print(response)
# print(json.keys())
# print(len(json))
# print(f'totalhits: {json["totalHits"]}')
# print(f'totalpages: {json["totalPages"]}')
# f=shelve.open[98]

# file = shelve.open('delete')
# file[str(page)] = json
# file.close()
# file = shelve.open('delete')
# json = file[str(page)]
# file.close()
# file = shelve.open('delete')
# file['other51'] = json
# file['squid'] = response
# file.close()
# file = shelve.open('delete')
# json = file['other51']
# file.close()
# f=shelve.open[98]

# file = shelve.open('delete')
# file['list'] = json
# file.close()
# file = shelve.open('delete')
# json = file['list']
# file.close()

# print(len(json))
# f=shelve.open[2]


#
# for entry in range(len(json)):
#     print(json['foods'][entry]['description'])
#
# df = pd.DataFrame(json['foods'])
# print(json['foods'][1].keys())
# print(json['foods'][1]['foodNutrients'])
# print(json['foods'][1]['foodNutrients'][22])
# print(df)

# for nutrient in range(len(json['foods'][1]['foodNutrients'])):
#     print(json['foods'][1]['foodNutrients'][nutrient]['nutrientName'])

# df = pd.DataFrame(json['foods'][1]['foodNutrients'])
# print(df.)


def food_search(api_key=None, food_item=None):
    if api_key is None:
        api_key = usda_key
    compare = {"total_entries": 0, "total_energy": 0, "total_carbs": 0}
    skip = ["Nong Shim Co., Ltd.", "Nasoya Foods USA, LLC",
            "United Natural Foods, Inc."]
    # print(json)
    # print(len(json))
    # f = shelve.open[3]
    query = "lasagna"
    end_search = ep().end_search(
        api_key="0arBG94hGw3XyzanWdsZ4I6dTCmsT1aj7QWSJkGf", query=query)
    params = end_search[1]
    url = end_search[0]
    food_query = requests.get(url, params=params)
    food_dict = {}  # add foods and their respective nutrients to dict
    food_l = []
    for food in food_query.json():
        # TODO: add some django handling here or something to sort by most recent later
        # pub_dates.append(food['publicationDate'])
        nutrients_unformat = food['foodNutrients']
        nutrients_clean = []
        name = [value['name'] for value in nutrients_unformat]
        amount = [value['amount'] for value in nutrients_unformat]
        unit = [value['unitName'] for value in nutrients_unformat]
        for name, amount, unit in zip(name, amount, unit):
            nutrients_clean.append("".join(f"{name}: {amount}{unit}"))
        food_l.append(
            {'description': food['description'], 'foodNutrients': nutrients_clean})
    # logic for sorting by publication date // pub_dates = sorted(pub_dates)
    if len(food_query.json()) < 1:
        return 'empty dict'
    else:
        return 'populated dict'

    # print(food_dict)

    # for entry in range(len(j_dict)):
    #     if j_dict['foods'][entry]['brandOwner'] in skip:
    #         continue
    #     if food_item in j_dict['foods'][entry]['description'].lower():
    #         # print(json['foods'][entry]['description'],end=" | ")
    #         # print(json['foods'][entry]['brandOwner'])
    #         # print(json['foods'][entry].keys())
    #         # print(len(json['foods'][entry]['foodNutrients']))
    #         # print(json['foods'][entry]['foodNutrients'])
    #                 # compare[f'{json["foods"][entry]["description"]}|{json["foods"][entry]["brandOwner"]}'] =
    #         for element in json['foods'][entry]['foodNutrients']:
    #             if element['nutrientName'] == 'Carbohydrate, by difference':
    #                 compare["total_entries"] += 1
    #                 compare['total_carbs'] += element["value"]
    #             if element['nutrientName'] == 'Energy':
    #                 compare["total_energy"] += element["value"]
    # avg_carbs = compare['total_carbs']/compare["total_entries"]
    # avg_energy = compare['total_energy']/compare["total_entries"]
    # print(f'Average Carbs: {avg_carbs} | Average Energy: {avg_energy}')
    # for entry in range(len(json)):
    #     if json['foods'][entry]['brandOwner'] in skip:
    #         continue
    #     if food_item in json['foods'][entry]['description'].lower():
    #         print(json['foods'][entry]['description'],end=" | ")
    #         print(json['foods'][entry]['brandOwner'])
    #         for element in json['foods'][entry]['foodNutrients']:
    #             if element['nutrientName'] == 'Carbohydrate, by difference':
    #                 print(f'Carbohydrate, by difference: {element["value"]} {element["unitName"]} | Percent difference from avg: {round((abs(element["value"]-avg_carbs)/avg_carbs)*100,2)}')
    #             if element['nutrientName'] == 'Energy':
    #                 print(f'Energy: {element["value"]} {element["unitName"]} | Percent difference from avg: {round((abs(element["value"]-avg_energy)/avg_energy)*100,2)}')
    # # df = pd.DataFrame(json['foods'][entry]['foodNutrients'])
    # # print(df)
    #     file.close()


# file = shelve.open('delete')
# json = file['other51']
# for key in [*json]:
#     if key == 'foods':
#         print(f'Amount of results:\n{len(json[key])}')
#         continue
#     print(f'{key}')
#     print(f'{json[key]}')
# print(json['foods'][0]['foodNutrients'])

# file = shelve.open('usda')
# nutrients = file['nutrientNames']
# file.close()
# print(len(nutrients))

# for entry in [*json['foods']]:
#     for ele in entry['foodNutrients']:
#         if ele['nutrientName'] not in nutrients:
#             nutrients.append(ele['nutrientName'])

# nutrients.sort()

# file = shelve.open('usda')
# file['nutrientNames'] = nutrients
# file.close()

# print(nutrients)
# for ele in nutrients:
#     print(ele)
# print(len(nutrients))
# df = pd.DataFrame(nutrients)
# print(df)
# for entry in [*json['foods']]:
#     for element in entry["foodNutrients"]:
#         print(len(entry["foodNutrients"]))
# print(element['nutrientName'])
# f=shelve.open[2]

# skip = ["organic","and","soup", "spicy", "&", "chicken", "beef", "rice", "pasta","chlorella", "miso","ginger","soy","tempura","shoyu","sanuki", "bowl"]
# skip = []
def holder():
    food_item = 'chicken'
    total_weight = {}
    data = {}
    data['percent_carbs'] = []
    for entry in [*data["foods"]]:
        # go = False
        # for ele in skip:
        #     if ele in entry['description'].lower():
        #         go = True
        # if go:
        #     continue
        if food_item in entry['description'].lower():
            total_weight["G"] = 0
            total_weight["MG"] = 0
            # print([*entry])
            # print(entry["foodNutrients"])
            for element in entry["foodNutrients"]:
                # print(element["unitName"])
                if element["nutrientName"] == "Carbohydrate, by difference":
                    carbs = element["value"]
                if element["unitName"] in [*total_weight]:
                    total_weight[element["unitName"]] += element['value']
            total = round(total_weight["G"] + (total_weight["MG"] / 1000), 2)
            percent_carbs = round((carbs / total) * 100, 2)
            data['percent_carbs'].append(percent_carbs)
            print(entry['description'])
            print(f'Total mass: {total} G | Percent Carbs: {percent_carbs}')
    # data["percent_carbs"].sort()
    # print(data["percent_carbs"])
    print(f'Highest Value: {max(data["percent_carbs"])}')
    print(f'Lowest Value: {min(data["percent_carbs"])}')
    print(
        f'Average Value: {round(sum(data["percent_carbs"]) / len(data["percent_carbs"]), 2)}')
    print(len(data["percent_carbs"]))
    # print(data["percent_carbs"])
    # data["percent_carbs"].remove(64.24)
    # print(f'Highest Value: {max(data["percent_carbs"])}')
    # print(f'Lowest Value: {min(data["percent_carbs"])}')
    # print(f'Average Value: {sum(data["percent_carbs"])/len(data["percent_carbs"])}')
    df = pd.DataFrame(data["percent_carbs"])
    print(df.mean())

    # Plotting
    x_axis = []
    for i in range(len(data["percent_carbs"])):
        x_axis.append(i)
    #
    y_axis = data["percent_carbs"]
    #
    # plt.scatter(x_axis, y_axis)
    # plt.ylabel('Percent Compositions')
    # plt.xlabel('Range')
    # plt.scatter(y_axis, x_axis)
    # plt.xlabel('Percent Compositions')
    # plt.ylabel('')
    # #
    # plt.show()


# Evaluate search results for x nutrient composition
class USDA(object):
    def __init__(self, key) -> None:
        super().__init__()
        self.key = key
        self.unit_names_bank = self.get_unit_names_bank()

    def search(self, query, data_type=f'SR%20Legacy', file_name='delete'):
        """
        Search the USDA nutrition API
        query: string
        data_type: string
        Acceptable data_types: "SR%20Legacy" (default) and "Branded"

        Returns: requests object
        """
        if not self.is_saved(file_key=query, file_name=file_name):
            url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={self.key}&query={query}&dataType={data_type}&pageSize=200'
            response = requests.get(url)
            if not response.ok:
                return f'{response.status_code}'
            print(response)
            self.save(item=response, file_key=query, file_name=file_name)

        response = self.get(file_key=query, file_name=file_name)
        json = response.json()
        print(f'Total Hits: {json["totalHits"]}')
        print(f'Total Pages: {json["totalPages"]}')
        self.results = json['foods']
        return response

    def save(self, item, file_key: str, file_name: str = 'delete'):
        """
        item: anything
        file_key: string
        """
        file = shelve.open(file_name)
        file[file_key] = item
        file.close()
        print('Saved')

    def get(self, file_key: str, file_name: str = 'delete'):
        file = shelve.open(file_name)
        item = file[file_key]
        file.close()
        return item

    def is_saved(self, file_key, file_name):
        file = shelve.open(file_name)
        try:
            if file[file_key]:
                file.close()
                return True
        except:
            file.close()
            return False

    def get_results(self):
        # print([*self.results[0]]) # delete
        return self.results

    def get_descriptions(self):
        descriptions = []
        for result in self.results:
            descriptions.append(result['description'])
        # print(descriptions)
        return descriptions

    def get_nutrient_names(self, description=None):
        nutrient_names = []
        if description:
            for nutrient in description[[*description][0]]:
                nutrient_names.append(nutrient['Nutrient Name'])
            return nutrient_names
        for result in self.results:
            for nutrient in result['foodNutrients']:
                if nutrient['nutrientName'] not in nutrient_names:
                    nutrient_names.append(nutrient['nutrientName'])
        # print(nutrient_names)
        return nutrient_names

    def get_nutrients(self, description=None):
        """
        Input: description: str

        Output: nutrients: dict[list]

        If description is specified, then returns nutrients[description] = [dict, ...]
        
        Else returns nutrients[every description in self.results] = [dict, ...]
        """
        nutrients = {}
        if description:
            nutrients[description] = []
            for result in self.results:
                if result['description'] == description:
                    for nutrient in result['foodNutrients']:
                        nutrients[description].append({
                            'Nutrient Name': nutrient['nutrientName'],
                            'Value': nutrient['value'],
                            'Unit': nutrient['unitName'],
                            'Nutrient ID': nutrient['nutrientId']
                        })
                    return nutrients
        for result in self.results:
            name = result['description']
            nutrients[name] = []
            for nutrient in result['foodNutrients']:
                nutrients[name].append(
                    {
                        'Nutrient Name': nutrient['nutrientName'],
                        'Value': nutrient['value'],
                        'Unit': nutrient['unitName'],
                        'Nutrient ID': nutrient['nutrientId']
                    })
        self.nutrients = nutrients
        # print(nutrients)
        return nutrients

    def get_total_mass(self, description):
        nutrients = self.get_nutrients(description=description)
        mass = 0
        for nutrient in nutrients[description]:
            if nutrient['Unit'] == 'G':
                mass += nutrient['Value']
            elif nutrient['Unit'] == 'MG':
                mass += nutrient['Value'] * 10 ** (-3)
            elif nutrient['Unit'] == 'UG':
                mass += nutrient['Value'] * 10 ** (-6)
            elif nutrient['Unit'] == 'IU':
                # print(f'Units not included(IU): {nutrient["Nutrient Name"]}')
                pass
        return round(mass, 3)

    def get_nutrient_composition(self, description, nutrient):
        total_mass = self.get_total_mass(description)
        for result in self.results:
            if result['description'] == description:
                for entry in result['foodNutrients']:
                    if entry['nutrientName'] == nutrient:
                        if entry['unitName'] in ['MG', 'UG']:
                            grams = self.convert_to_grams(
                                entry['value'], entry['unitName'])
                        elif entry['unitName'] == 'G':
                            grams = entry['value']
                        else:
                            continue
                        # if grams == 0:
                        #     continue
                        # print(description)
                        composition = grams / total_mass * 100
                        composition = round(composition, 3)
                        return composition

    def convert_to_grams(self, value, unit):
        unit = unit.lower()
        if unit == 'mg':
            return value * 10 ** (-3)
        elif unit == 'ug':
            return value * 10 ** (-6)

    def convert_to_calories(self, value, unit):
        unit = unit.lower()
        if unit == 'kj':
            return value / 4.184

    def get_nutrient_names_bank(self):
        file = shelve.open('../../USDA')
        bank = file['nutrient_names_bank']
        file.close()
        return bank

    def get_unit_names_bank(self):
        file = shelve.open('../../USDA')
        bank = file['unit_names_bank']
        file.close()
        return bank

    def get_daily_nutrition(self, age=None, sex=None):
        file = shelve.open('../../USDA')
        daily_nutrition_bank = file['daily_nutrition']
        file.close()
        if not age and not sex:  # if no age or sex specified
            return daily_nutrition_bank
        for age_range in [*daily_nutrition_bank[sex]]:
            if age in range(age_range[0], age_range[1] + 1):
                return daily_nutrition_bank[sex][age_range]

    def eval_nutrient_composition(self, food_item):
        food_item = 'bread'
        total_weight = {}
        data = {}
        data['percent_carbs'] = []
        for entry in [*json["foods"]]:
            if food_item in entry['description'].lower():
                total_weight["G"] = 0
                total_weight["MG"] = 0
                for element in entry["foodNutrients"]:
                    if element["nutrientName"] == "Carbohydrate, by difference":
                        carbs = element["value"]
                    if element["unitName"] in [*total_weight]:
                        total_weight[element["unitName"]] += element['value']
                total = round(total_weight["G"] +
                              (total_weight["MG"] / 1000), 2)
                percent_carbs = round((carbs / total) * 100, 2)
                data['percent_carbs'].append(percent_carbs)
                print(entry['description'])
                print(
                    f'Total mass: {total} G | Percent Carbs: {percent_carbs}')
        print(f'Highest Value: {max(data["percent_carbs"])}')
        print(f'Lowest Value: {min(data["percent_carbs"])}')
        print(
            f'Average Value: {round(sum(data["percent_carbs"]) / len(data["percent_carbs"]), 2)}')
        print(len(data["percent_carbs"]))
        df = pd.DataFrame(data["percent_carbs"])
        print(df.mean())


def percent_difference():
    pass


# Print functions
# usda_pages save/open
# file = shelve.open('usda_pages')
# file[str(page)] = json
# file.close()
# file = shelve.open('usda_pages')
# json = file['16']
# file.close()

# print(json)
# print(json[0])
# print(len(json))
# print(list(json.keys()))
# print(len(json.keys()))
# print(json['foods'])
# print(len(json['foods']))
# print(json['foods'][6]['description'])

# For entry iteration
# for entry in range(len(json)):
#     print(json[entry]['description'])

# Specific item search
# food_item = 'chicken sandwich'
# for page in range(1,51):
#     file = shelve.open('usda_pages')
#     json = file[f'{page}']
#     for entry in range(len(json)):
#         if food_item in json[entry]['description'].lower():
#             print(json[entry]['description'])
#             df = pd.DataFrame(json[entry]['foodNutrients'])
#             print(df)
#     file.close()
nutrient_dict = {
    "Alanine": "",
    "Alcohol, ethyl": "",
    "Arginine": "",
    "Ash": "",
    "Aspartic acid": "",
    "Beta-sitosterol": "",
    "Betaine": "",
    "Caffeine": "",
    "Calcium, Ca": "",
    "Campesterol": "",
    "Carbohydrate, by difference": "",
    "Carotene, alpha": "",
    "Carotene, beta": "",
    "Cholesterol": "",
    "Choline, total": "",
    "Copper, Cu": "",
    "Cryptoxanthin, beta": "",
    "Cystine": "",
    "Energy": "",
    "Fatty acids, total monounsaturated": "",
    "Fatty acids, total polyunsaturated": "",
    "Fatty acids, total saturated": "",
    "Fatty acids, total trans": "",
    "Fatty acids, total trans-monoenoic": "",
    "Fatty acids, total trans-polyenoic": "",
    "Fiber, total dietary": "",
    "Fluoride, F": "",
    "Folate, DFE": "",
    "Folate, food": "",
    "Folate, total": "",
    "Folic acid": "",
    "Fructose": "",
    "Galactose": "",
    "Glucose (dextrose)": "",
    "Glutamic acid": "",
    "Glycine": "",
    "Histidine": "",
    "Hydroxyproline": "",
    "Iron, Fe": "",
    "Isoleucine": "",
    "Lactose": "",
    "Leucine": "",
    "Lutein + zeaxanthin": "",
    "Lycopene": "",
    "Lysine": "",
    "MUFA 14:1": "",
    "MUFA 15:1": "",
    "MUFA 16:1": "",
    "MUFA 16:1 c": "",
    "MUFA 17:1": "",
    "MUFA 18:1": "",
    "MUFA 18:1 c": "",
    "MUFA 18:1-11 t (18:1t n-7)": "",
    "MUFA 20:1": "",
    "MUFA 22:1": "",
    "MUFA 22:1 c": "",
    "MUFA 24:1 c": "",
    "Magnesium, Mg": "",
    "Maltose": "",
    "Manganese, Mn": "",
    "Methionine": "",
    "Niacin": "",
    "PUFA 18:2": "",
    "PUFA 18:2 CLAs": "",
    "PUFA 18:2 i": "",
    "PUFA 18:2 n-6 c,c": "",
    "PUFA 18:3": "",
    "PUFA 18:3 n-3 c,c,c (ALA)": "",
    "PUFA 18:3 n-6 c,c,c": "",
    "PUFA 18:3i": "",
    "PUFA 18:4": "",
    "PUFA 20:2 n-6 c,c": "",
    "PUFA 20:3": "",
    "PUFA 20:3 n-3": "",
    "PUFA 20:3 n-6": "",
    "PUFA 20:4": "",
    "PUFA 21:5": "",
    "PUFA 22:4": "",
    "PUFA 22:5 n-3 (DPA)": "",
    "PUFA 22:6 n-3 (DHA)": "",
    "PUFA 2:4 n-6": "",
    "PUFA 2:5 n-3 (EPA)": "",
    "Pantothenic acid": "",
    "Phenylalanine": "",
    "Phosphorus, P": "",
    "Phytosterols": "",
    "Potassium, K": "",
    "Proline": "",
    "Protein": "",
    "Retinol": "",
    "Riboflavin": "",
    "SFA 10:0": "",
    "SFA 12:0": "",
    "SFA 13:0": "",
    "SFA 14:0": "",
    "SFA 15:0": "",
    "SFA 16:0": "",
    "SFA 17:0": "",
    "SFA 18:0": "",
    "SFA 20:0": "",
    "SFA 22:0": "",
    "SFA 24:0": "",
    "SFA 4:0": "",
    "SFA 6:0": "",
    "SFA 8:0": "",
    "Selenium, Se": "",
    "Serine": "",
    "Sodium, Na": "",
    "Starch": "",
    "Stigmasterol": "",
    "Sucrose": "",
    "Sugars, total including NLEA": "",
    "TFA 16:1 t": "",
    "TFA 18:1 t": "",
    "TFA 18:2 t not further defined": "",
    "TFA 18:2 t,t": "",
    "TFA 22:1 t": "",
    "Theobromine": "",
    "Thiamin": "",
    "Threonine": "",
    "Tocopherol, beta": "",
    "Tocopherol, delta": "",
    "Tocopherol, gamma": "",
    "Tocotrienol, alpha": "",
    "Tocotrienol, beta": "",
    "Tocotrienol, delta": "",
    "Tocotrienol, gamma": "",
    "Total lipid (fat)": "",
    "Tryptophan": "",
    "Tyrosine": "",
    "Valine": "",
    "Vitamin A, IU": "",
    "Vitamin A, RAE": "",
    "Vitamin B-12": "",
    "Vitamin B-12, added": "",
    "Vitamin B-6": "",
    "Vitamin C, total ascorbic acid": "",
    "Vitamin D (D2 + D3)": "",
    "Vitamin D (D2 + D3), International Units": "",
    "Vitamin D2 (ergocalciferol)": "",
    "Vitamin D3 (cholecalciferol)": "",
    "Vitamin E (alpha-tocopherol)": "",
    "Vitamin E, added": "",
    "Vitamin K (Dihydrophylloquinone)": "",
    "Vitamin K (Menaquinone-4)": "",
    "Vitamin K (phylloquinone)": "",
    "Water": "",
    "Zinc, Zn": ""
}
nutrients = [
    "['Protein: 10.6G', 'Total lipid (fat): 12.9G', 'Carbohydrate, by difference: 35.3G', 'Energy: 306KCAL', 'Sugars, total including NLEA: 4.71G', 'Fiber, total dietary: 1.2G', 'Calcium, Ca: 176MG', 'Iron, Fe: 1.69MG', 'Sodium, Na: 847MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 29.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 5.29G']",
    "['Protein: 7.89G', 'Total lipid (fat): 0.0G', 'Carbohydrate, by difference: 55.3G', 'Energy: 263KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 2.6G', 'Calcium, Ca: 0.0MG', 'Iron, Fe: 0.95MG', 'Sodium, Na: 553MG', 'Vitamin A, IU: 0.0IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 0.0MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 0.0G']",
    "['Protein: 21.4G', 'Total lipid (fat): 25.0G', 'Carbohydrate, by difference: 0.0G', 'Energy: 346KCAL', 'Sugars, total including NLEA: 0.0G', 'Fiber, total dietary: 0.0G', 'Calcium, Ca: 714MG', 'Iron, Fe: 0.0MG', 'Sodium, Na: 536MG', 'Vitamin A, IU: 714IU', 'Vitamin C, total ascorbic acid: 0.0MG', 'Cholesterol: 146MG', 'Fatty acids, total trans: 0.0G', 'Fatty acids, total saturated: 14.3G']",
    "['Protein: 10.4G', 'Total lipid (fat): 20.8G', 'Carbohydrate, by difference: 44.8G', 'Energy: 408KCAL', 'Alcohol, ethyl: 0.0G', 'Water: 21.1G', 'Caffeine: 0.0MG', 'Theobromine: 0.0MG', 'Sugars, total including NLEA: 2.08G', 'Fiber, total dietary: 2.1G', 'Calcium, Ca: 90.0MG', 'Iron, Fe: 2.49MG', 'Magnesium, Mg: 17.0MG', 'Phosphorus, P: 120MG', 'Potassium, K: 84.0MG', 'Sodium, Na: 750MG', 'Zinc, Zn: 0.96MG', 'Copper, Cu: 0.086MG', 'Selenium, Se: 19.8UG', 'Retinol: 23.0UG', 'Vitamin A, RAE: 24.0UG', 'Carotene, beta: 9.0UG', 'Carotene, alpha: 1.0UG', 'Vitamin E (alpha-tocopherol): 1.49MG', 'Vitamin D (D2 + D3): 0.1UG', 'Cryptoxanthin, beta: 0.0UG', 'Lycopene: 0.0UG', 'Lutein + zeaxanthin: 45.0UG', 'Vitamin C, total ascorbic acid: 0.0MG', 'Thiamin: 0.433MG', 'Riboflavin: 0.303MG', 'Niacin: 3.28MG', 'Vitamin B-6: 0.048MG', 'Folate, total: 107UG', 'Vitamin B-12: 0.24UG', 'Choline, total: 8.5MG', 'Vitamin K (phylloquinone): 32.4UG', 'Folic acid: 75.0UG', 'Folate, food: 32.0UG', 'Folate, DFE: 159UG', 'Vitamin E, added: 0.0MG', 'Vitamin B-12, added: 0.0UG', 'Cholesterol: 10.0MG', 'Fatty acids, total saturated: 6.25G', 'SFA 4:0: 0.153G', 'SFA 6:0: 0.073G', 'SFA 8:0: 0.043G', 'SFA 10:0: 0.096G', 'SFA 12:0: 0.111G', 'SFA 14:0: 0.401G', 'SFA 16:0: 3.62G', 'SFA 18:0: 1.48G', 'MUFA 18:1: 4.17G', 'PUFA 18:2: 8.1G', 'PUFA 18:3: 1.1G', 'PUFA 20:4: 0.0G', 'PUFA 22:6 n-3 (DHA): 0.0G', 'MUFA 16:1: 0.076G', 'PUFA 18:4: 0.0G', 'MUFA 20:1: 0.039G', 'PUFA 2:5 n-3 (EPA): 0.0G', 'MUFA 22:1: 0.0G', 'PUFA 22:5 n-3 (DPA): 0.0G', 'Fatty acids, total monounsaturated: 4.34G', 'Fatty acids, total polyunsaturated: 9.2G']"
]

for n in nutrients:
    a = ast.literal_eval(n)
    # print(a)

names = list((nutrient.split(':') for nutrient in nutrients))
for name in names:
    nutrient = name[0]
    amount = name[1].strip(" ")
    # print(nutrient, amount)
new_dict = {}
for k, v in nutrient_dict.items():
    if k == None:
        new_dict.update({k: '55'})

res = [list(filter(lambda ele: ele in sub, nutrient_dict))
       for sub in nutrients]
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
# print(nutrient_balance)

goal = {
    'calories': {
        'Calories': 2400},
    'macronutrients': {
        'Protein (% kcal)': '10-35',
        'Protein (g)': 56,
        'Carbohydrate (% kcal)': '45-65',
        'Carbohydrate (g)': 130,
        'Fiber (g)': 34,
        'Added Sugars (% kcal)': '<10',
        'Total lipid (% kcal)': '20-35',
        'Saturated Fatty Acids (% kcal)': '<10',
        '18:2 Linoleic acid (g)': 17,
        '18:3 Linoleic acid (g)': 1.6},
    'minerals': {
        'Calcium (mg)': 1000,
        'Iron (mg)': 8,
        'Magnesium (mg)': 400,
        'Phosphorus (mg)': 700,
        'Potassium (mg)': 3400,
        'Sodium (mg)': 2300,
        'Zinc (mg)': 11},
    'vitamins': {
        'Vitamin A (mcg RAE)': 900,
        'Vitamin E (mg AT)': 15,
        'Vitamin D (IU)': 600,
        'Vitamin C (mg)': 90,
        'Thiamin (mg)': 1.2,
        'Riboflavin (mg)': 1.3,
        'Niacin (mg)': 16,
        'Vitamin B-6 (mg)': 1.3,
        'Vitamin B-12 (mcg)': 2.4,
        'Choline (mg)': 550,
        'Vitamin K (mcg)': 120,
        'Folate (mcg DFE)': 400
    }
}
nutrient_balance = {
    'Protein': 50.29,
    'Total lipid (fat)': 58.7,
    'Carbohydrate, by difference': 135.39999999999998,
    'Energy': 1323.0,
    'Sugars, total including NLEA': 6.79,
    'Fiber, total dietary': 5.9,
    'Calcium, Ca': 980.0,
    'Iron, Fe': 5.13,
    'Sodium, Na': 2686.0,
    'Vitamin A, IU': 714.0,
    'Vitamin C, total ascorbic acid': 0.0,
    'Cholesterol': 185.0,
    'Fatty acids, total trans': 0.0,
    'Fatty acids, total saturated': 25.84,
    'Alcohol, ethyl': 0.0, 'Water': 21.1,
    'Caffeine': 0.0, 'Theobromine': 0.0,
    'Magnesium, Mg': 17.0,
    'Phosphorus, P': 120.0,
    'Potassium, K': 84.0,
    'Zinc, Zn': 0.96,
    'Copper, Cu': 0.086,
    'Selenium, Se': 19.8,
    'Retinol': 23.0,
    'Vitamin A, RAE': 24.0,
    'Carotene, beta': 9.0,
    'Carotene, alpha': 1.0,
    'Vitamin E (alpha-tocopherol)': 1.49,
    'Vitamin D (D2 + D3)': 0.1,
    'Cryptoxanthin, beta': 0.0,
    'Lycopene': 0.0,
    'Lutein + zeaxanthin': 45.0,
    'Thiamin': 0.433,
    'Riboflavin': 0.303,
    'Niacin': 3.28,
    'Vitamin B-6': 0.048,
    'Folate, total': 107.0,
    'Vitamin B-12': 0.24,
    'Choline, total': 8.5,
    'Vitamin K (phylloquinone)': 32.4,
    'Folic acid': 75.0,
    'Folate, food': 32.0,
    'Folate, DFE': 159.0,
    'Vitamin E, added': 0.0,
    'Vitamin B-12, added': 0.0,
    'SFA 4:0': 0.153,
    'SFA 6:0': 0.073,
    'SFA 8:0': 0.043,
    'SFA 10:0': 0.096,
    'SFA 12:0': 0.111,
    'SFA 14:0': 0.401,
    'SFA 16:0': 3.62,
    'SFA 18:0': 1.48,
    'MUFA 18:1': 4.17,
    'PUFA 18:2': 8.1,
    'PUFA 18:3': 1.1,
    'PUFA 20:4': 0.0,
    'PUFA 22:6 n-3 (DHA)': 0.0,
    'MUFA 16:1': 0.076,
    'PUFA 18:4': 0.0,
    'MUFA 20:1': 0.039,
    'PUFA 2:5 n-3 (EPA)': 0.0,
    'MUFA 22:1': 0.0,
    'PUFA 22:5 n-3 (DPA)': 0.0,
    'Fatty acids, total monounsaturated': 4.34,
    'Fatty acids, total polyunsaturated': 9.2
}
nutrient_balance = {
    "Alcohol, ethyl": 0.0,
    "Ash": 4.74,
    "Caffeine": 0.0,
    "Calcium, Ca": 93.0,
    "Carbohydrate, by difference": 46.29,
    "Carotene, alpha": 0.0,
    "Carotene, beta": 7.0,
    "Cholesterol": 49.0,
    "Choline, total": 7.5,
    "Copper, Cu": 0.107,
    "Cryptoxanthin, beta": 0.0,
    "Energy": 2383.0,
    "Fatty acids, total monounsaturated": 4.609999999999999,
    "Fatty acids, total polyunsaturated": 6.76,
    "Fatty acids, total saturated": 4.38,
    "Fatty acids, total trans": 0.093,
    "Fatty acids, total trans-monoenoic": 0.063,
    "Fatty acids, total trans-polyenoic": 0.03,
    "Fiber, total dietary": 2.4,
    "Folate, DFE": 233.0,
    "Folate, food": 24.0,
    "Folate, total": 147.0,
    "Folic acid": 123.0,
    "Fructose": 0.0,
    "Galactose": 0.0,
    "Glucose": 0.0,
    "Iron, Fe": 5.25,
    "Lactose": 0.0,
    "Lutein + zeaxanthin": 10.0,
    "Lycopene": 0.0,
    "MUFA 14:1": 0.021,
    "MUFA 15:1": 0.0,
    "MUFA 16:1": 0.167,
    "MUFA 16:1 c": 0.06,
    "MUFA 17:1": 0.009,
    "MUFA 18:1": 4.35,
    "MUFA 18:1 c": 2.57,
    "MUFA 20:1": 0.053,
    "MUFA 22:1": 0.002,
    "MUFA 22:1 c": 0.0,
    "MUFA 24:1 c": 0.0,
    "Magnesium, Mg": 42.0,
    "Maltose": 1.11,
    "Manganese, Mn": 0.488,
    "Niacin": 7.08,
    "PUFA 18:2": 5.970000000000001,
    "PUFA 18:2 CLAs": 0.018,
    "PUFA 18:2 n-6 c,c": 5.36,
    "PUFA 18:3": 0.774,
    "PUFA 18:3 n-3 c,c,c (ALA)": 0.696,
    "PUFA 18:3 n-6 c,c,c": 0.028,
    "PUFA 18:3i": 0.0,
    "PUFA 18:4": 0.0,
    "PUFA 20:2 n-6 c,c": 0.004,
    "PUFA 20:3": 0.003,
    "PUFA 20:3 n-3": 0.0,
    "PUFA 20:4": 0.01,
    "PUFA 20:4 n-6": 0.003,
    "PUFA 20:5 n-3 (EPA)": 0.004,
    "PUFA 22:4": 0.002,
    "PUFA 22:5 n-3 (DPA)": 0.002,
    "PUFA 22:6 n-3 (DHA)": 0.0,
    "Pantothenic acid": 0.39,
    "Phosphorus, P": 129.0,
    "Potassium, K": 674.0,
    "Protein": 30.0,
    "Retinol": 23.0,
    "Riboflavin": 0.56,
    "SFA 10:0": 0.042,
    "SFA 12:0": 0.061,
    "SFA 14:0": 0.271,
    "SFA 15:0": 0.025,
    "SFA 16:0": 2.66,
    "SFA 17:0": 0.023,
    "SFA 18:0": 1.1360000000000001,
    "SFA 20:0": 0.032,
    "SFA 22:0": 0.022,
    "SFA 24:0": 0.014,
    "SFA 4:0": 0.038,
    "SFA 6:0": 0.028,
    "SFA 8:0": 0.016,
    "Selenium, Se": 22.0,
    "Sodium, Na": 1129.0,
    "Starch": 38.8,
    "Sucrose": 0.0,
    "Sugars, total including NLEA": 1.33,
    "TFA 16:1 t": 0.007,
    "TFA 18:1 t": 0.054,
    "TFA 18:2 t not further defined": 0.03,
    "TFA 22:1 t": 0.002,
    "Theobromine": 0.0,
    "Thiamin": 0.493,
    "Total lipid (fat)": 17.060000000000002,
    "Vitamin A, IU": 88.0,
    "Vitamin A, RAE": 24.0,
    "Vitamin B-12": 0.13,
    "Vitamin B-12, added": 0.0,
    "Vitamin B-6": 0.103,
    "Vitamin C, total ascorbic acid": 1.7,
    "Vitamin D (D2 + D3)": 0.0,
    "Vitamin D (D2 + D3), International Units": 2.0,
    "Vitamin E (alpha-tocopherol)": 0.88,
    "Vitamin E, added": 0.0,
    "Vitamin K (Dihydrophylloquinone)": 0.0,
    "Vitamin K (Menaquinone-4)": 1.1,
    "Vitamin K (phylloquinone)": 21.1,
    "Water": 101.9,
    "Zinc, Zn": 2.3200000000000003
    }
goal_dict = {
    "Protein": 46,
    "Carbohydrate": 130,
    "Fiber": 25,
    "18:2 Linoleic acid": 12,
    "18:3 Linoleic acid": 1.1,
    "Calcium": 1000,
    "Iron": 18,
    "Magnesium": 320,
    "Phosphorus": 700,
    "Potassium": 2600,
    "Sodium": 2300,
    "Zinc": 8,
    "Vitamin A": 700,
    "Vitamin E": 15,
    "Vitamin D": 600,
    "Vitamin C": 75,
    "Thiamin": 1.1,
    "Riboflavin": 1.1,
    "Niacin": 14,
    "Vitamin B-6": 1.3,
    "Vitamin B-12": 2.4,
    "Choline": 425,
    "Vitamin K": 90,
    "Folate": 400
  }
nutrient_balance = {
    "Alanine": 2.567,
    "Alcohol, ethyl": 0.0,
    "Arginine": 2.9110000000000005,
    "Ash": 8.18,
    "Aspartic acid": 4.361,
    "Betaine": 0.7,
    "Caffeine": 0.0,
    "Calcium, Ca": 317.0,
    "Carbohydrate, by difference": 181.36,
    "Carotene, alpha": 0.0,
    "Carotene, beta": 1423.0,
    "Cholesterol": 779.0,
    "Choline, total": 496.7,
    "Copper, Cu": 0.426,
    "Cryptoxanthin, beta": 18.0,
    "Cystine": 0.781,
    "Energy": 4048.0,
    "Fatty acids, total monounsaturated": 20.233,
    "Fatty acids, total polyunsaturated": 9.027000000000001,
    "Fatty acids, total saturated": 22.181999999999995,
    "Fatty acids, total trans": 0.076,
    "Fiber, total dietary": 9.200000000000001,
    "Fluoride, F": 2.2,
    "Folate, DFE": 205.0,
    "Folate, food": 205.0,
    "Folate, total": 205.0,
    "Folic acid": 0.0,
    "Fructose": 0.0,
    "Galactose": 0.0,
    "Glucose": 0.74,
    "Glutamic acid": 6.359999999999999,
    "Glycine": 2.1060000000000003,
    "Histidine": 1.125,
    "Iron, Fe": 10.280000000000001,
    "Isoleucine": 2.242,
    "Lactose": 0.0,
    "Leucine": 3.526,
    "Lutein + zeaxanthin": 4570.0,
    "Lycopene": 0.0,
    "Lysine": 3.186,
    "MUFA 14:1": 0.014,
    "MUFA 15:1": 0.0,
    "MUFA 16:1": 0.799,
    "MUFA 17:1": 0.024,
    "MUFA 18:1": 9.26,
    "MUFA 20:1": 0.139,
    "MUFA 22:1": 0.0,
    "MUFA 24:1 c": 0.0,
    "Magnesium, Mg": 114.0,
    "Maltose": 0.0,
    "Manganese, Mn": 0.948,
    "Methionine": 1.2120000000000002,
    "Niacin": 7.460999999999999,
    "PUFA 18:2": 4.653,
    "PUFA 18:3": 0.32800000000000007,
    "PUFA 18:4": 0.0,
    "PUFA 20:2 n-6 c,c": 0.036,
    "PUFA 20:3": 0.046,
    "PUFA 20:4": 0.41600000000000004,
    "PUFA 20:5 n-3 (EPA)": 0.014,
    "PUFA 22:4": 0.026,
    "PUFA 22:5 n-3 (DPA)": 0.021,
    "PUFA 22:6 n-3 (DHA)": 0.131,
    "Pantothenic acid": 4.567,
    "Phenylalanine": 2.1050000000000004,
    "Phosphorus, P": 635.0,
    "Phytosterols": 5.0,
    "Potassium, K": 1913.0,
    "Proline": 2.0300000000000002,
    "Protein": 63.36,
    "Retinol": 318.0,
    "Riboflavin": 0.955,
    "SFA 10:0": 0.012,
    "SFA 12:0": 0.011,
    "SFA 14:0": 0.14100000000000001,
    "SFA 15:0": 0.016,
    "SFA 16:0": 6.430000000000001,
    "SFA 17:0": 0.042,
    "SFA 18:0": 2.084,
    "SFA 20:0": 0.006,
    "SFA 22:0": 0.008,
    "SFA 24:0": 0.0,
    "SFA 4:0": 0.008,
    "SFA 6:0": 0.0,
    "SFA 8:0": 0.008,
    "Selenium, Se": 80.0,
    "Serine": 2.673,
    "Sodium, Na": 4781.0,
    "Sucrose": 0.0,
    "Sugars, added": 3.4,
    "Sugars, total including NLEA": 17.8,
    "Theobromine": 0.0,
    "Thiamin": 0.23099999999999998,
    "Threonine": 1.8730000000000002,
    "Tocopherol, beta": 0.02,
    "Tocopherol, delta": 0.12,
    "Tocopherol, gamma": 1.02,
    "Tocotrienol, alpha": 0.12,
    "Tocotrienol, beta": 0.0,
    "Tocotrienol, delta": 0.0,
    "Tocotrienol, gamma": 0.02,
    "Total lipid (fat)": 54.14,
    "Tryptophan": 0.543,
    "Tyrosine": 1.5939999999999999,
    "Valine": 2.6449999999999996,
    "Vitamin A, IU": 3450.0,
    "Vitamin A, RAE": 439.0,
    "Vitamin B-12": 1.66,
    "Vitamin B-12, added": 0.0,
    "Vitamin B-6": 1.03,
    "Vitamin C, total ascorbic acid": 23.0,
    "Vitamin D (D2 + D3)": 4.0,
    "Vitamin D (D2 + D3), International Units": 164.0,
    "Vitamin D3 (cholecalciferol)": 4.0,
    "Vitamin E (alpha-tocopherol)": 2.6600000000000006,
    "Vitamin E, added": 0.0,
    "Vitamin K (Dihydrophylloquinone)": 0.2,
    "Vitamin K (phylloquinone)": 110.9,
    "Water": 472.7,
    "Zinc, Zn": 4.51
  }
if __name__ == '__main__':
    print(food_search("lasagna"))
