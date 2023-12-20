from config.db import PyObjectId
from pydantic import ConfigDict, BaseModel, Field
from typing import Optional, List
from bson import ObjectId

class ExperienciaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    empresa: str = Field(...)
    cargo: str = Field(...)
    startYear: int = Field(...)
    endYear: Optional[int] = Field(default=None)
    descripcion: Optional[str] = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example":{
                "empresa": "Upwork",
                "cargo": "Contratista (Freelancer)",
                "startYear": 2020,
                "endYear": 2023,
                "descripcion": "Trabajo como asistente virtual manejando Microsoft Office y GSuite"
            }
        }
    )

class UpdateExperienciaModel(BaseModel):
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    startYear: Optional[int] = None
    endYear: Optional[int] = None
    descripcion: Optional[int]
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example":{
                "empresa": "Upwork",
                "cargo": "Contratista (Freelancer)",
                "startYear": 2020,
                "endYear": 2023,
                "descripcion": "Trabajo como asistente virtual manejando Microsoft Office y GSuite"
            }
        }
    )

class ExperienciaCollection(BaseModel):
    experiencia: List[ExperienciaModel]