from config.db import PyObjectId
from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId

class EducacionModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titulo: str = Field(...)
    tipo: str = Field(...)
    institucion: str = Field(...)
    startYear: int = Field(...)
    endYear: Optional[int] = Field(default=None)
    minor: Optional[str] = Field(default=None)
    description: str = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titulo": "Comercio Internacional",
                "tipo": "Licenciatura",
                "institucion": "Universidad Alejandro de Humboldt",
                "startYear": 2018,
                "endYear": 2022,
                "description": "Importaciones y exportaciones"
            }
        }
    )

class UpdateEducacionModel(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    institucion: Optional[str] = None
    startYear: Optional[int] = None
    endYear: Optional[int] = None
    minor: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "titulo": "Comercio Internacional",
                "tipo": "Licenciatura",
                "institucion": "Universidad Alejandro de Humboldt",
                "startYear": 2018,
                "endYear": 2022,
                "description": "Importaciones y exportaciones"
            }
        }
    )

class EducacionCollection(BaseModel):
    educacion: List[EducacionModel]