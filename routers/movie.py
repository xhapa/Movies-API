#Python
from typing import Optional, List

#FastAPI
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import Body, Query, Path, Depends
from fastapi.responses import JSONResponse

#Models
from models.movie import Movie as MovieModel

#Config
from config.database import Session

#Schemas
from schemas.movie import Movie 

#Middlewares
from middlewares.jwt_bearer import JWTBearer

#Services
from services.movie import MovieService

movie_router = APIRouter()

# Movies page
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies() -> List[Movie]:
    db = Session()
    movies = MovieService(db).get_movies()
    return jsonable_encoder(movies)

@movie_router.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
async def get_movie(
    movie_id: int = Path(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    )
) -> Movie:
    db = Session()
    movie = MovieService(db).get_movie(movie_id=movie_id)
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@movie_router.get('/movies/', tags=['movies'])
async def get_movies_by_category(
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
    db = Session()
    movies = MovieService(db).get_movies_by_category(category=category)
    if not movies:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@movie_router.get('/movie/detail', tags=['movies'], response_model=List[Movie])
async def get_movie_by_category(
    category: str = Query(
        ...,
        max_length=50,
        min_length=1,
        title="Movie category",
        description="This is the movie category"
    )
) -> List[Movie]:
    db = Session()
    movie = MovieService(db).get_movie_by_category(category=category)
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
async def create_movie(
    movie: Movie = Body(...)
):
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Movie added"})

@movie_router.put('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
async def update_movie(
    movie_id: int = Path(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    ),
    movie: Movie = Body(...)
):  
    db = Session()
    result = MovieService(db).valid_movie(movie_id=movie_id)
    if not result:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    MovieService(db).update_movie(result, movie)
    return JSONResponse(content={"message": "Movie modified"}) 

@movie_router.delete('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
async def delete_movie(
    movie_id: int = Path(
        ...,
        ge=0,
        title="Movie ID",
        description="This is the movie ID"  
    )
):
    db = Session()
    movie = MovieService(db).valid_movie(movie_id=movie_id)
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    MovieService(db).delete_movie(movie)
    return JSONResponse(content={"message": "Movie deleted"}) 
