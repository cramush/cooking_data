import json
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.dialects.postgresql import JSON
from pprint import pprint
import config


# with open('data.json', 'r') as f:
#     recipesss = json.load(f)
#     pprint(recipesss)

url = f'postgresql+psycopg2://{config.login}:{config.password}@{config.host}/{config.db_name}'
engine = create_engine(url, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
Base = declarative_base()


class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    ingredients = Column(JSON, nullable=False)
    cooking_time = Column(String(20), nullable=False)
    nutrition = relationship("Nutrition")


class Nutrition(Base):
    __tablename__ = "nutrition"
    id = Column(BigInteger, nullable=False, primary_key=True)
    proteins = Column(String(10), nullable=False)
    fats = Column(String(10), nullable=False)
    carbohydrates = Column(String(10), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete='CASCADE'))


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)
s = session()

raw_res = {
    "id": 138933,
    "title": "Салат из чечевицы с молодой свеклой, радиккио и фундуком",
    "description": "Вместо радиккио можно добавить руколу или даже молодую крапиву — поверьте, она очень вкусная! Что касается средиземноморских травок, то и розмарин, и орегано, и тимьян для таких салатов подходят идеально, причем как свежие, так и сухие. А еще хорошо добавить смесь перца, растереть кориандр, тмин или зиру — все это будет здесь очень кстати!",
    "ingredients": '''{
        "свекла молодая": "9 г",
        "чечевица красная": "25 г",
        "радиккио": "26 г",
        "салатный микс": "4 шт.",
        "подсушенный фундук": "150 г",
        "розмарин": "⅙  кочана",
        "тимьян": "70 г",
        "чеснок": "1 горсть",
        "оливковое масло": "2 веточки",
        "перец чили молотый": "6 веточек",
        "перец черный свежемолотый": "2 зубчика",
        "соль морская": "4 ст. л.",
        "лимоны": "1 щепотка",
        "оливковое масло Extra Virgin": "1 щепотка",
        "мед жидкий": "1 щепотка",
        "горчица русская": "½  шт.",
        "уксус с эстрагоном": "3 ст. л."
    }''',
    "cooking_time": 40,
}
raw_nut = {
    "fats": "25 г",
    "proteins": "9 г",
    "carbohydrates": "26 г",
    "recipe_id": raw_res["id"],
}

res = Recipes(**raw_res)
nut = Nutrition(**raw_nut)
s.add(res)
s.add(nut)
s.commit()
pprint("++++++++++++++++++++++++++++++++++")
pprint(nut.id)

# s.query(Nutrition).delete()
s.query(Recipes).delete()
s.commit()


