#Python
from typing import Optional, List

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

#Own----------------------------------------------------------------------------

#Models
from models.movie import Movie as MovieModel
from models.user import User as UserModel

#Middlewares
from jwt_manager import create_token
from security import JWTBearer

#Config
from config.database import Session, Base, engine

#Schemas
from schemas.movie import Movie 
from schemas.user import User


# Movies App -------------------------------------------------------------------
app = FastAPI()
app.title = "My app"
app.version = "0.0.2"

Base.metadata.create_all(bind= engine)

# Home page
@app.get('/')
async def message():
    return HTMLResponse('<h1>Hello World</h1>')

# Auth page
@app.post('/login', tags=['auth'])
async def login(
    user: User = Body(...)
):  
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

# Movies page
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies() -> List[Movie]:
    db = Session()
    movies = db.query(MovieModel).all()
    return jsonable_encoder(movies)

@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
async def get_movie(
    movie_id: int = Path(
        ...,
        gt=0,
        title="Movie ID",
        description="This is the movie ID"
    )
) -> Movie:
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@app.get('/movies/', tags=['movies'])
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
    movies = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not movies:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@app.get('/movie/detail', tags=['movies'], response_model=List[Movie])
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
    movie = db.query(MovieModel).filter(MovieModel.category == category).first()
    if not movie:
        return JSONResponse(status_code= 404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
async def create_movie(
    movie: Movie = Body(...)
):
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie added"})

@app.put('/movies/{movie_id}', tags=['movies'], response_model=dict, status_code=200)
async def update_movie(
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
async def delete_movie(
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