from datetime import timedelta

from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from config.db import users_collection
from models.usersModel import UserModel, UsersCollection, UpdateUserModel
from models.tokenModel import TokenData
from bson import ObjectId
from passlib.context import CryptContext
from pymongo import ReturnDocument
from config.auth import validate_user
from typing import Annotated
from config.jwthandler import create_access_token, get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get(
    '/me',
    description="Retorna un usuario si esta autenticado",
    response_model_by_alias=False
)
async def user_me(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autenticación fallida')
    return {'user': user}

@router.post(
    '/registrar',
    description="Registrar un usuario",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    # dependencies=[Depends(get_current_user)]
)
async def create_user(user: UserModel = Body(...)):
    user.password = pwd_context.encrypt(user.password)

    if (
        existe_usuario := await users_collection.find_one({"email": user.email}) or await users_collection.find_one({"email": user.username})
    ) is not None:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.post('/token', response_model=TokenData)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await validate_user(form_data)

    token = create_access_token(user['username'], timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}