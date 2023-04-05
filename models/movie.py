#Sqlalchemy
from sqlalchemy import Column, Integer, Float, String

#Own
from config.database import Base

#Model
class Movie(Base):

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer) 
    rating = Column(Float)
    category = Column(String)