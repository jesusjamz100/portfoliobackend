from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from models.usersModel import UserModel
from config.db import users_collection

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    return await users_collection.find_one({"username": username})

async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    if (
        db_user := await get_user(user.username)
    ) is None:
        raise HTTPException(
            status_code=401,
            detail="Contraseña o usuario incorrecto"
        )

    if not verify_password(user.password, db_user['password']):
        raise HTTPException(
            status_code=401,
            detail="Contraseña o usuario incorrecto"
        )
    
    return db_user