from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.dialects.postgresql import JSON
import config


url = f'postgresql+psycopg2://{config.login}:{config.password}@{config.host}/{config.db_name}'
engine = create_engine(url, echo=False)
if not database_exists(engine.url):
    create_database(engine.url)
Base = declarative_base()


class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(250), nullable=False) # сделать уникальным
    description = Column(TEXT, nullable=False)
    ingredients = Column(JSON, nullable=False)
    portions = Column(Integer, nullable=False)
    cooking_time = Column(JSON, nullable=False)
    nutrition = relationship("Nutrition")
    calories = relationship("Calories")
    steps = relationship("Steps")


class Nutrition(Base):
    __tablename__ = "nutrition"
    id = Column(BigInteger, nullable=False, primary_key=True)
    proteins = Column(String(10), nullable=False)
    fats = Column(String(10), nullable=False)
    carbohydrates = Column(String(10), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete='CASCADE'))


class Calories(Base):
    __tablename__ = "calories"
    id = Column(BigInteger, nullable=False, primary_key=True)
    value = Column(Integer, nullable=False)
    unit = Column(String(10), nullable=False)
    percent = Column(Integer, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete='CASCADE'))


class Steps(Base):
    __tablename__ = "steps"
    id = Column(BigInteger, nullable=False, primary_key=True)
    step_number = Column(Integer, nullable=True)
    description = Column(TEXT)
    img = Column(String(50), nullable=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete='CASCADE'))


def rewrite_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    rewrite_tables()

