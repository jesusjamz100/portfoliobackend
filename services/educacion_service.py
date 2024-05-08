from fastapi import Response, HTTPException
from repositories.educacion_repository import EducacionRepository
from models.educacion_model import EducacionCollection, EducacionModel, UpdateEducacionModel
from config.db import educacion_collection
from pymongo import ReturnDocument
from bson import ObjectId

class EducacionService:
    
    def __init__(self) -> None:
        self.repository = EducacionRepository()

    async def get_all_educacion(self) -> EducacionCollection:
        return await self.repository.get_all()

    async def get_educacion_by_id(self, id: str) -> EducacionModel:
        return await self.repository.get_by_id(id)

    async def save_educacion(self, educacion: EducacionModel) -> EducacionModel:
        return await self.repository.save(educacion)
    
    async def delete_educacion(self, id: str) -> Response:
        return await self.repository.delete_by_id(id)
    
    async def update_educacion(self, id: str, educacion: UpdateEducacionModel) -> EducacionModel:
        educacion = {
            k: v for k, v in educacion.model_dump(by_alias=True).items() if v is not None
        }

        if len(educacion) >= 1:
            update_result = await educacion_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": educacion},
                return_document=ReturnDocument.AFTER
            )
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'Educacion {id} no fue encontrada')
            
        if (existing_educacion := await educacion_collection.find_one({"_id": id})) is not None:
            return existing_educacion
        
        raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")