#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My app"
app.version = "0.0.1"

movies = []

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
    movie_id: int = Path(...)
):
    for movie in movies:
        if movie.id ==  movie_id:
            return movie
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(
    category: str = Query(...),
    year: Optional[int] = Query(None)
):
    return category

@app.get('/movie/detail', tags=['movies'])
def get_movie_by_category(
    category: str = Query(...)
):
    return [movie for movie in movies if movie.category== category]

@app.post('/movies', tags=['movies'])
def create_movie(
    movie: Movie = Body(...)
):
    movies.append(movie)
    return movies

@app.put('/movies/{movie_id}', tags=['movies'])
def update_movie(
    movie_id: int = Path(...),
    movie: Movie = Body(...)
):
    for idx, item in enumerate(movies):
        if item.id == movie_id:
            movies[idx] = movie

    return movies 

@app.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(
    movie_id: int = Path(...)
):
    for movie in movies:
        if movie.id == movie_id:
            movies.remove(movie)
            return movies