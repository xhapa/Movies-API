#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#Models
class Movie(BaseModel):
    id: int = Field(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="Movie title",
        description="This is the movie title"
    )
    overview: str = Field(
        ...,
        min_length=1,
        max_length=400,
        title="Movie Overview",
        description="This is the movie overview"
    )
    year: int = Field(
        ...,
        gt=0,
        le=2023,
        title="Movie year",
        description="This is the movie year"
    )
    rating: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        title="Movie rating",
        description="This is the movie rating"
    )
    category: str = Field(
        ...,
        max_length=50,
        min_length=1,
        title="Movie category",
        description="This is the movie category"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": 'Ant-Man and the Wasp: Quantumania',
                "overview": "Ant-Man and the Wasp find themselves exploring the Quantum Realm, interacting with strange new creatures and embarking on an adventure that pushes them beyond the limits of what they thought was possible.",
                "year": 2023,
                "rating": 9.2,
                "category": "Adventure/Action"
            }
        }

class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
