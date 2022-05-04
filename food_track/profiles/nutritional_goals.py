import json


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

    def __init__(self) -> None:
        with open('daily_nutrient_goals.json') as data:
            self.nutrition = json.load(data)

    def __str__(self) -> str:
        return self.nutrition

    def get_daily_nutrition(self, age=None, sex=None):
        """
        Input: age int, sex str
        Output: nutrition{
            "calories":{},
            "macronutrients":{},
            "minerals":{},
            "vitamins:{}
            }
        """
        if not age and not sex:
            return self.nutrition
        # Handle age exceptions 
        if age < 2 or age > 130:
            return "Invalid age. Valid range is 2-130."
        # If age and sex not given, return entire table
        for age_range in [*self.nutrition[sex]]:
            split = age_range.split("-")
            lower, upper = int(split[0]), int(split[1]) + 1
            if age in range(lower, upper):
                return self.nutrition[sex][age_range]
