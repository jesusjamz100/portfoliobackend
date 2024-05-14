from config.db import PyObjectId
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from typing import Optional, List
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(max_length=15)
    password: str = Field(min_length=6)
    email: EmailStr = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "username",
                "password": "password",
                "email": "correo@correo.com"
            }
        }
    )

class UpdateUserModel(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "username",
                "password": "password",
                "email": "correo@correo.com"
            }
        }
    )

class UsersCollection(BaseModel):
    users: List[UserModel]