import json
import os


class DailyNutrients(object):
    """
    A class to help with getting appropriate daily nutritional goals.

    ...

    Attributes
    ------------
    nutrition : dict
        dictionary of nutritional goals sectioned out by sex, then age group

    Methods
    ------------
    get_daily_nutrition(age=None, sex=None):
        returns dictionary of daily nutrition based on given age and sex.
    """

    def __init__(self, age=None, sex=None) -> None:
        self.age = age
        self.sex = sex
        os.chdir('./profiles/static/json')
        with open('nutrient_data.json') as data:
            self.nutrition = json.load(data)["daily_nutrient_goals"]
        os.chdir('../../../')

    def __str__(self) -> str:
        return self.nutrition

    def get_daily_nutrition(self):
        """
        Input: age int, sex str
        Output: nutrition{
            "calories":{},
            "macronutrients":{},
            "minerals":{},
            "vitamins:{}
            }
        """
        if not self.age and not self.sex:
            return self.nutrition
        # Handle age exceptions 
        if self.age < 2 or self.age > 130:
            return "Invalid age. Valid range is 2-130."
        # If age and sex not given, return entire table
        for age_range in [*self.nutrition[self.sex]]:
            split = age_range.split("-")
            lower, upper = int(split[0]), int(split[1]) + 1
            if self.age in range(lower, upper):
                return self.nutrition[self.sex][age_range]

    def get_nutrient_names_bank(self):
        """Gets all possible nutrient names.

        Returns:
            list: nutrient names
        """
        os.chdir('./profiles/static/json')
        with open('nutrient_data.json') as data:
            self.nutrient_names_bank = json.load(data)["nutrient_names_bank"]
        os.chdir('../../../')
        return self.nutrient_names_bank
    
    def get_goal_names_bank(self):
        """Gets list that is used as an intermediary to process between goals, and
        all possible nutrient variations.

        Returns:
            dictionary: "nutrient names": [variant1, variant2, etc.]
        """
        os.chdir('./profiles/static/json')
        with open('nutrient_data.json') as data:
            self.goal_names_bank = json.load(data)["goal_names_bank"]
        os.chdir('../../../')
        return self.goal_names_bank


