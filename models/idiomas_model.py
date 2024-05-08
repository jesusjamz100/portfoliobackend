from config.db import PyObjectId
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from bson import ObjectId

class IdiomaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    language: str = Field(...)
    nivel: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "language": "Inglés",
                "nivel": "Bilingüe"
            }
        }
    )

class UpdateIdiomaModel(BaseModel):
    language: Optional[str] = None
    nivel: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "language": "Inglés",
                "nivel": "Bilingüe"
            }
        }
    )

class IdiomaCollection(BaseModel):
    idiomas: List[IdiomaModel]