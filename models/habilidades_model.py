from config.db import PyObjectId
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from bson import ObjectId

class HabilidadModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    habilidad: str = Field(...)
    tipo: str = Field(...)
    nivel: int = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "habilidad": "Python",
                "tipo": "dura",
                "nivel": 3
            }
        }
    )

class UpdateHabilidadModel(BaseModel):
    habilidad: Optional[str] = None
    tipo: Optional[str] = None
    nivel: Optional[int] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "habilidad": "Python",
                "tipo": "dura",
                "nivel": 3
            }
        }
    )

class HabilidadesCollection(BaseModel):
    habilidades: List[HabilidadModel]