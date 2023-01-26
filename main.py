#Python

#Pydantic

#FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My app"
app.version = "0.0.1"




@app.get('/')
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies/', tags=['movies'])
def get_movies():
    return movies