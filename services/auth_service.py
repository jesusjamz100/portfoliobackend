from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from config.db import users_collection

class AuthService:
     
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def get_user(self, username: str):
        return await users_collection.find_one({"username": username})

    async def validate_user(self, user: OAuth2PasswordRequestForm = Depends()):
        if (
            db_user := await self.get_user(user.username)
        ) is None:
            raise HTTPException(
                status_code=401,
                detail="Contraseña o usuario incorrecto"
            )

        if not self.verify_password(user.password, db_user['password']):
            raise HTTPException(
                status_code=401,
                detail="Contraseña o usuario incorrecto"
            )
        
        return db_user