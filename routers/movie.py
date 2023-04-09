#Python
from typing import Annotated

#FastAPI
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import Body, Query, Path, Depends, Response
from fastapi.responses import JSONResponse

#Config
from config.database import Session

#Schemas
from schemas.movie import Movie 

#Middlewares
from middlewares.jwt_bearer import JWTBearer

#Services
from services.movie import MovieService

movie_router = APIRouter(prefix='/movies', tags=["Movies"])

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Movies page
@movie_router.get('/', response_model=None, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies(db: Session = Depends(get_db)) -> JSONResponse:
    movies = MovieService(db).get_movies()
    return JSONResponse(status_code=200 ,content= jsonable_encoder(movies))

@movie_router.get('/{movie_id}', response_model=None)
async def get_movie(
    movie_id: Annotated[
        int, 
        Path(
            gt=0,
            title="Movie ID",
            description="This is the movie ID"
        )
    ] = ...,
    db: Session = Depends(get_db)
) -> Response:
    movie = MovieService(db).get_movie(movie_id=movie_id)
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200 ,content= jsonable_encoder(movie))

@movie_router.get('/', response_model=None)
async def get_movies_by_category(
    category: Annotated[
        str | None, 
        Query(
            max_length=50,
            min_length=1,
            title="Movie category",
            description="This is the movie category"
        )
    ] = None,
    year: Annotated[
        int | None, 
        Query(
            gt=0,
            le=2023,
            title="Movie year",
            description="This is the movie year"
        )
    ] = None,
    db: Session = Depends(get_db)
)-> Response:
    movies = MovieService(db).get_movies_by_category(category=category)
    if not movies:
        return JSONResponse(status_code= 404, content={'message': 'Movie, Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@movie_router.get('/detail', response_model=None)
async def get_movie_by_category(
    category: Annotated[
        str | None, 
        Query(
            max_length=50,
            min_length=1,
            title="Movie category",
            description="This is the movie category"
        )
    ] = None,
    db: Session = Depends(get_db)
) -> Response:
    movie = MovieService(db).get_movie_by_category(category=category)
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Movie, Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@movie_router.post('/new', response_model=Movie, status_code=201)
async def create_movie(
    movie: Annotated[Movie, Body()] = ...,
    db: Session = Depends(get_db)
)-> Movie:
    MovieService(db).create_movie(movie)
    return movie

@movie_router.put('/{movie_id}', response_model=None, status_code=200)
async def update_movie(
    movie_id: Annotated[
        int, 
        Path(
            gt=0,
            title="Movie ID",
            description="This is the movie ID"
        )
    ] = ...,
    movie: Annotated[Movie, Body()] = ...,
    db: Session = Depends(get_db)
)-> Response:  
    result = MovieService(db).valid_movie(movie_id=movie_id)
    if not result:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    MovieService(db).update_movie(result, movie)
    return JSONResponse(content={"message": "Movie modified"}) 

@movie_router.delete('/{movie_id}', response_model=None, status_code=200)
async def delete_movie(
    movie_id: Annotated[
        int, 
        Path(
            gt=0,
            title="Movie ID",
            description="This is the movie ID"
        )
    ] = ...,
    db: Session = Depends(get_db)
)-> Response:
    movie = MovieService(db).valid_movie(movie_id=movie_id)
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    MovieService(db).delete_movie(movie)
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))
