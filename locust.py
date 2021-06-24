from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import config
from crud import Recipes, Nutrition, Calories, Steps


url = f'postgresql+psycopg2://{config.login}:{config.password}@{config.host}/{config.db_name}'
engine = create_engine(url, echo=False)
if not database_exists(engine.url):
    create_database(engine.url)

session = sessionmaker(bind=engine)
s = session()


def create_recipes(raw_data):
    recipe_data = {
        "id": raw_data["id"],
        "title": raw_data["title"],
        "description": raw_data["description"],
        "ingredients": raw_data["ingredients"],
        "portions": raw_data["portions"],
        "cooking_time": raw_data["cooking_time"]
    }
    s.add(Recipes(**recipe_data))
    s.commit()


def create_nutrition(nut_data, data_id):
    nutritions = {
        "proteins": nut_data["Белки"],
        "fats": nut_data["Жиры"],
        "carbohydrates": nut_data["Углеводы"],
        "recipe_id": data_id,
    }
    s.add(Nutrition(**nutritions))
    s.commit()


def create_calories(cal_data, data_id):
    calories = {"recipe_id": data_id}
    calories.update(cal_data)
    s.add(Calories(**calories))
    s.commit()


def create_steps(steps_data, data_id):
    for step_number, contents in steps_data.items():
        step = {
            "recipe_id": data_id,
            "step_number": step_number,
        }
        step.update(contents)
        s.add(Steps(**step))

    s.commit()


