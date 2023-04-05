
#Sqlalchemy
from sqlalchemy import Column, Integer, Float, String

#Own
from config.database import Base

#Model
class User(Base):

    __tablename__ = 'user'

    user = Column(String, primary_key = True)
    email = Column(String)
    password = Column(String)