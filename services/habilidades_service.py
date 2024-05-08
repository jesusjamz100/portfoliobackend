from fastapi import Response, HTTPException
from config.db import habilidades_collection
from repositories.habilidades_repository import HabilidadesRepository
from models.habilidades_model import HabilidadModel, HabilidadesCollection, UpdateHabilidadModel
from bson import ObjectId
from pymongo import ReturnDocument

class HabilidadesService:

    def __init__(self) -> None:
        self.repository = HabilidadesRepository()

    async def get_all_habilidades(self) -> HabilidadesCollection:
        return await self.repository.get_all()
    
    async def get_habilidad_by_id(self, id: str) -> HabilidadModel:
        return await self.repository.get_by_id(id)
    
    async def save_habilidad(self, habilidad: HabilidadModel) -> HabilidadModel:
        return await self.repository.save(habilidad)

    async def delete_habilidad(self, id: str) -> Response:
        return await self.repository.delete_by_id(id)
    
    async def update_habilidad(self, id: str, habilidad: UpdateHabilidadModel) -> HabilidadModel:
        habilidad = {
            k: v for k, v in habilidad.model_dump(by_alias=True).items() if v is not None
        }

        if len(habilidad) >= 1:
            update_result = await habilidades_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": habilidad},
                return_document=ReturnDocument.AFTER
            )
            if update_result is not None:
                return update_result
            else:
                HTTPException(status_code=404, detail=f'Habilidad {id} no encontrada')
        
        if (existing_habilidad := await habilidades_collection.find_one({"_id": id})) is not None:
            return existing_habilidad
        
        raise HTTPException(status_code=404, detail=f'Habilidad {id} no encontrada')