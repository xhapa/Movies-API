#Pydantic
from pydantic import BaseModel
from pydantic import Field

class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)