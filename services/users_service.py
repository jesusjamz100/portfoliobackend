from fastapi import HTTPException
from repositories.users_repository import UserRepository
from models.users_model import UserModel
from passlib.context import CryptContext

class UserService:

    def __init__(self) -> None:
        self.repository = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def add_user(self, user: UserModel) -> UserModel:
        user.password = self.pwd_context.encrypt(user.password)
        if (
            existe_usuario := await self.repository.get_by_email(user.email) or await self.repository.get_by_username(user.username)
        ) is not None:
            raise HTTPException(status_code=400, detail="El usuario ya existe")