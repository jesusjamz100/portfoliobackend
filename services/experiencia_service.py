from fastapi import Response, HTTPException, status
from config.db import experiencia_collection
from repositories.experiencia_repository import ExperienciaRepository
from models.experiencia_model import ExperienciaModel, ExperienciaCollection, UpdateExperienciaModel
from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.results import DeleteResult

class ExperienciaService:

    def __init__(self) -> None:
        self.repository = ExperienciaRepository()

    async def get_all_experiencia(self) -> ExperienciaCollection:
        return await self.repository.get_all()
    
    async def get_experiencia_by_id(self, id: str) -> ExperienciaModel:
        experiencia = await self.repository.get_by_id(id)
        if experiencia:
            return experiencia
        raise HTTPException(status_code=404, detail=f"La experiencia con ID: {id} no se encuentra")
    
    async def save_experiencia(self, experiencia: ExperienciaModel) -> ExperienciaModel:
        return await self.repository.save(experiencia)
    
    async def delete_experiencia(self, id: str) -> Response:
        delete_result: DeleteResult = await self.repository.delete_by_id(id)
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=404, detail=f"Experiencia {id} no encontrada")
    
    async def update_experiencia(self, id: str, experiencia: UpdateExperienciaModel) -> ExperienciaModel:
        experiencia = {
            k: v for k, v in experiencia.model_dump(by_alias=True).items() if v is not None
        }

        if len(experiencia) >= 1:
            update_result = await self.repository.update_by_id(id, experiencia)
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'Experiencia {id} no encontrada')
        
        if (existing_experiencia := await self.repository.get_by_id(id))  is not None:
            return existing_experiencia
        
        raise HTTPException(status_code=404, detail=f"Experiencia {id} no encontrada")