from typing import Optional

from pydantic import BaseModel

class TokenData(BaseModel):
    access_token: str
    token_type: str

class Status(BaseModel):
    message: str