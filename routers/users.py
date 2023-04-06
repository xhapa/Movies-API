#FastAPI
from fastapi import APIRouter
from fastapi import Body, Query, Path, Depends
from fastapi.responses import JSONResponse

#Schemas
from schemas.user import User

#Middleware
from middlewares.jwt_manager import create_token

users_router = APIRouter()

# Auth page
@users_router.post('/login', tags=['auth'])
async def login(
    user: User = Body(...)
):  
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)