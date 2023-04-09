#Python
from typing import Annotated

#FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi.responses import JSONResponse

#Schemas
from schemas.user import User

#Middleware
from middlewares.jwt_manager import create_token

users_router = APIRouter(prefix='/users', tags=["Auth"])

# Auth page
@users_router.post('/login', status_code=200, response_model=None)
async def login(
    user: Annotated[User, Body(..., embed=True)]
)-> JSONResponse:  
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=400, content={'message' : 'User not valid'})