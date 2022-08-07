import json

class Populator():
    def import_sr_legacy(self):
        data = open("FoodData_Central_sr_legacy_food_json_2021-10-28.json")
        data = json.load(data)
        srlegacyfoods = data["SRLegacyFoods"]
        count = 0
        for entry in srlegacyfoods:
            # Name
            name = entry['description']

            # Food Category
            food_category = entry['foodCategory']['description']

            # fdcId
            fdc_id = entry['fdcId']
            
            # Publication Date
            publication_date = entry['publicationDate']
            publication_date = publication_date.split('/')
            for i, n in enumerate(publication_date):
                publication_date[i] = int(n)
            year = publication_date[2]
            day = publication_date[1]
            if day < 10:
                day = f'0{day}'
            month = publication_date[0]    
            if month < 10:
                month = f'0{month}'
            publication_date = f'{year}-{month}-{day}'

            # Nutrients
            nutrient_list = []
            for nutriententry in entry['foodNutrients']:
                element = ""
                nutrient_name = nutriententry['nutrient']['name']
                id = str(nutriententry['nutrient']['id'])
                amount = str(nutriententry['amount'])
                unitname = nutriententry['nutrient']['unitName']
                if unitname == "Âµg":
                    unitname = 'ug'
                element = f'{nutrient_name} ({id}): {amount}{unitname}'
                nutrient_list.append(element)
            nutrient_list.sort()

            SRLegacy.objects.create(
                name=name,
                category=food_category,
                fdc_id=fdc_id,
                publication_date=publication_date,
                nutrients=nutrient_list
            )
            count += 1
            print(f'Finished SRLegacy: {count}')
            
    def import_branded(self):
        data = open("FoodData_Central_branded_food_json_2022-04-28.json", encoding='mbcs')
        data = json.load(data)
        brandedfoods = data["BrandedFoods"]
        count = 0
        for entry in brandedfoods:
            # Brand name
            brandOwner = entry['brandOwner']

            # Name
            name = entry['description']

            # fdcId
            fdc_id = entry['fdcId']

            # Food Category
            food_category = entry['brandedFoodCategory']
            
            # Publication Date
            publication_date = entry['publicationDate']
            publication_date = publication_date.split('/')
            for i, n in enumerate(publication_date):
                publication_date[i] = int(n)
            year = publication_date[2]
            day = publication_date[1]
            if day < 10:
                day = f'0{day}'
            month = publication_date[0]    
            if month < 10:
                month = f'0{month}'
            publication_date = f'{year}-{month}-{day}'

            # marketCountry
            marketCountry = entry['marketCountry']

            # Nutrients
            nutrient_list = []
            for nutriententry in entry['foodNutrients']:
                element = ""
                nutrient_name = nutriententry['nutrient']['name']
                id = str(nutriententry['nutrient']['id'])
                amount = str(nutriententry['amount'])
                unitname = nutriententry['nutrient']['unitName']
                if unitname == "Âµg":
                    unitname = 'ug'
                element = f'{nutrient_name} ({id}): {amount}{unitname}'
                nutrient_list.append(element)
            nutrient_list.sort()
            
            # Ingredients
            ingredients = entry['ingredients']
            Branded.objects.create(
                brandOwner=brandOwner,
                name=name,
                fdc_id=fdc_id,
                category=food_category,
                publication_date=publication_date,
                marketCountry=marketCountry,
                nutrients=nutrient_list,
                ingredients=ingredients
            )
            count += 1
            print(f'Finished Branded: {count}')