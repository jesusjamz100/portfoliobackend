from config.db import PyObjectId
from pydantic import BaseModel, Field, ConfigDict, AnyUrl
from typing import Optional, List
from bson import ObjectId

class ProyectoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titulo: str = Field(...)
    descripcion: str = Field(...)
    tecnologias: list = Field(...)
    startDate: str = Field(...)
    endDate: Optional[str] = Field(default=None)
    githubLinks: Optional[list] = Field(default=None)
    deployLinks: Optional[list] = Field(default=None)
    imgUrl: Optional[str] = Field(default=None)
    model_config=ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titulo": "Manejo de condominio",
                "descripcion": "Aplicacion Full-Stack para el manejo de un condominio",
                "tecnologias": ["Python", "Flask", "SqlAlchemy", "React", "Axios"],
                "startDate": "2023-11-03",
                "endDate": "2023-12-03",
                "githubLinks": [
                    "https://www.github.com/backend",
                    "https://www.github.com/backend"
                ],
                "deployLinks": [
                    "https://ejemplo.com"
                ]
            }
        }
    )

class UpdateProyectoModel(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tecnologias: Optional[list] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    githubLinks: Optional[list] = None
    deployLinks: Optional[list] = None
    model_config=ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "titulo": "Manejo de condominio",
                "descripcion": "Aplicacion Full-Stack para el manejo de un condominio",
                "tecnologias": ["Python", "Flask", "SqlAlchemy", "React", "Axios"],
                "startDate": "2023-11-03",
                "endDate": "2023-12-03",
                "githubLinks": [
                    "https://www.github.com/backend",
                    "https://www.github.com/backend"
                ],
                "deployLinks": [
                    "https://ejemplo.com"
                ]
            }
        }
    )

class ProyectosCollection(BaseModel):
    proyectos: List[ProyectoModel]