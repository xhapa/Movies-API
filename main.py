#Uvicorn
import uvicorn
import os

#FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

#Config
from config.database import Base, engine

#Middleware
from middlewares.error_handler import ErrorHandler

#Routers
from routers.movie import movie_router
from routers.users import users_router

# Movies App -------------------------------------------------------------------
app = FastAPI()
app.title = "My app"
app.version = "0.0.3"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(users_router)

Base.metadata.create_all(bind= engine)

# Home page
@app.get('/')
async def message():
    return HTMLResponse('<h1>Hello World</h1>')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)))