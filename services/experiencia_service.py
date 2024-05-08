from fastapi import Response, HTTPException
from config.db import experiencia_collection
from repositories.experiencia_repository import ExperienciaRepository
from models.experiencia_model import ExperienciaModel, ExperienciaCollection, UpdateExperienciaModel
from bson import ObjectId
from pymongo import ReturnDocument

class ExperienciaService:

    def __init__(self) -> None:
        self.repository = ExperienciaRepository()

    async def get_all_experiencia(self) -> ExperienciaCollection:
        return await self.repository.get_all()
    
    async def get_experiencia_by_id(self, id: str) -> ExperienciaModel:
        return await self.repository.get_by_id(id)
    
    async def save_experiencia(self, experiencia: ExperienciaModel) -> ExperienciaModel:
        return await self.repository.save(experiencia)
    
    async def delete_experiencia(self, id: str) -> Response:
        return await self.repository.delete_by_id(id)
    
    async def update_experiencia(self, id: str, experiencia: UpdateExperienciaModel) -> ExperienciaModel:
        experiencia = {
            k: v for k, v in experiencia.model_dump(by_alias=True).items() if v is not None
        }
        if len(experiencia) >= 1:
            update_result = await experiencia_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": experiencia},
                return_document=ReturnDocument.AFTER
            )
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'Experiencia {id} no encontrada')
        
        if (existing_experiencia := await experiencia_collection.find_one({"_id": id}))  is not None:
            return existing_experiencia
        
        raise HTTPException(status_code=404, detail=f"Experiencia {id} no encontrada")