from locust import create_recipes, create_nutrition, create_calories, create_steps
from crud import rewrite_tables
from os.path import join, dirname
from os import listdir
import json


def bon_appetite(data):
    data_id = data["id"]
    create_recipes(data)
    create_nutrition(data["nutrition"], data_id)
    create_calories(data["calories"], data_id)
    create_steps(data["steps"], data_id)


if __name__ == '__main__':
    rewrite_tables()
    data_dir = join(dirname(__file__), "data")
    dir_list = listdir(data_dir)
    for d in dir_list:
        print(d)
        data_file_path = join(data_dir, d, 'data.json')
        with open(data_file_path, 'r') as f:
            data = json.load(f)
        bon_appetite(data)
