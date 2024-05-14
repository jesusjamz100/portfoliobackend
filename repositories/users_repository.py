from fastapi import HTTPException, Response, status
from config.db import users_collection
from models.users_model import UserModel
from bson import ObjectId
from pymongo.results import InsertOneResult
from typing import Optional

class UserRepository:

    async def get_by_id(self, id: str) -> Optional[UserModel]:
        return await users_collection.find_one({"_id": ObjectId(id)})
    
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        return await users_collection.find_one({"email": email})
    
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        return await users_collection.find_one({"username": username})
    
    async def save(self, user: UserModel) -> UserModel:
        new_user: InsertOneResult = await users_collection.insert_one(
            user.model_dump(by_alias=True, exclude=["id"])
        )
        created_user = await users_collection.find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user