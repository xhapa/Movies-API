#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My app"
app.version = "0.0.1"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

#Models
class Movie(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    overview: str = Field(...)
    year: int = Field(...)
    rating: Optional[float] = Field(default=None)
    category: str = Field(...)

@app.get('/')
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{movie_id}', tags=['movies'])
def get_movie(
    movie_id: int
):
    for movie in movies:
        if movie['id'] ==  movie_id:
            return movie
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(
    category: str,
    year: int
):
    return category

@app.get('/movie/detail', tags=['movies'])
def get_movie_by_category(
    category: str
):
    return [movie for movie in movies if movie['category'] == category]