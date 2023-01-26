#Python
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
app.title = "My app"
app.version = "0.0.2"

movies = []

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

@app.get('/')
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return movies

@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
def get_movie(
    movie_id: int = Field(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    )
) -> Movie:
    for movie in movies:
        if movie.id ==  movie_id:
            return movie
    return JSONResponse(content=[])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(
    category: str = Query(
        ...,
        max_length=50,
        min_length=1,
        title="Movie category",
        description="This is the movie category"
    ),
    year: Optional[int] = Query(
        None,
        gt=0,
        le=2023,
        title="Movie year",
        description="This is the movie year"
    )
):
    return category

@app.get('/movie/detail', tags=['movies'], response_model=List[Movie])
def get_movie_by_category(
    category: str = Query(
        ...,
        max_length=50,
        min_length=1,
        title="Movie category",
        description="This is the movie category"
    )
) -> List[Movie]:
    return [movie for movie in movies if movie.category== category]

@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(
    movie: Movie = Body(...)
):
    movies.append(movie)
    return JSONResponse(content={"message": "Movie added"})

@app.put('/movies/{movie_id}', tags=['movies'], response_model=dict)
def update_movie(
    movie_id: int = Field(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    ),
    movie: Movie = Body(...)
):
    for idx, item in enumerate(movies):
        if item.id == movie_id:
            movies[idx] = movie

    return JSONResponse(content={"message": "Movie modified"}) 

@app.delete('/movies/{movie_id}', tags=['movies'], response_model=dict)
def delete_movie(
    movie_id: int = Path(
        ...,
        ge=0,
        title="Movie ID",
        description="This is the movie ID"  
    )
):
    for movie in movies:
        if movie.id == movie_id:
            movies.remove(movie)
            return JSONResponse(content={"message": "Movie deleted"}) 