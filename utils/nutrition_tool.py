import requests
import os
from langchain.tools import BaseTool

class NutritionAPI:
    def __init__(self):
        self.api_key = os.getenv("API_NINJAS_KEY")
        self.api_url = "https://api.api-ninjas.com/v1/nutrition?query="

    def get_nutrition_data(self, item: str):
        headers = {"X-Api-Key": self.api_key}
        res = requests.get(self.api_url + item, headers=headers)
        if res.status_code == 200:
            data = res.json()
            return data[0] if data else {}
        return {}

# LangChain Tool Wrappers
class NutritionTool(BaseTool):
    name = "GetNutritionInfo"
    description = "Fetches nutrition info (calories, protein, fat, carbs) for a given food item."

    def _run(self, query: str):
        api = NutritionAPI()
        data = api.get_nutrition_data(query)
        if not data:
            return "No data found."
        return (
            f"**{data['name'].title()}**:\n"
            f"- Calories: {data['calories']} kcal\n"
            f"- Protein: {data['protein_g']} g\n"
            f"- Fat: {data['fat_total_g']} g\n"
            f"- Carbs: {data['carbohydrates_total_g']} g"
        )

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented.")

class CalorieTool(BaseTool):
    name = "GetCaloriesOnly"
    description = "Returns only the calorie value for a food item"

    def _run(self, query: str):
        api = NutritionAPI()
        data = api.get_nutrition_data(query)
        return data.get("calories", 0)

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented.")

class MacroTool(BaseTool):
    name = "GetMacroBreakdown"
    description = "Returns only the macros: protein, fat, carbs"

    def _run(self, query: str):
        api = NutritionAPI()
        data = api.get_nutrition_data(query)
        return {
            "protein": data.get("protein_g", 0),
            "fat": data.get("fat_total_g", 0),
            "carbs": data.get("carbohydrates_total_g", 0)
        }

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented.")
