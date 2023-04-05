#Python
from typing import Optional, List

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Depends
from fastapi.responses import HTMLResponse, JSONResponse

#Own
from jwt_manager import create_token
from models import Movie, User
from security import JWTBearer

# Movies App -------------------------------------------------------------------
app = FastAPI()
app.title = "My app"
app.version = "0.0.2"

movies = []

# Home page
@app.get('/')
def message():
    return HTMLResponse('<h1>Hello World</h1>')

# Auth page
@app.post('/login', tags=['auth'])
def login(
    user: User = Body(...)
):  
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

# Movies page
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return movies

@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
def get_movie(
    movie_id: int = Path(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    )
) -> Movie:
    for movie in movies:
        if movie.id ==  movie_id:
            return movie
    return JSONResponse(status_code=404, content=[])

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

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(
    movie: Movie = Body(...)
):
    movies.append(movie)
    return JSONResponse(content={"message": "Movie added"})

@app.put('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(
    movie_id: int = Path(
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

@app.delete('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
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