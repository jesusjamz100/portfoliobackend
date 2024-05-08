from fastapi import HTTPException, Response, status
from config.db import experiencia_collection
from models.experiencia_model import ExperienciaModel, ExperienciaCollection
from bson import ObjectId
from pymongo.results import DeleteResult

class ExperienciaRepository:

    async def get_all(self) -> ExperienciaCollection:
        return ExperienciaCollection(experiencia=await experiencia_collection.find().to_list(1000))
    
    async def get_by_id(self, id: str) -> ExperienciaModel:
        if (
            experiencia := await experiencia_collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return experiencia
        raise HTTPException(status_code=404, detail=f"La experiencia con ID: {id} no se encuentra")
    
    async def save(self, experiencia: ExperienciaModel) -> ExperienciaModel:
        new_experiencia = await experiencia_collection.insert_one(
            experiencia.model_dump(by_alias=True, exclude=["id"])
        )
        created_experiencia = await experiencia_collection.find_one(
            {"_id": new_experiencia.inserted_id}
        )
        return created_experiencia
    
    async def delete_by_id(self, id: str):
        delete_result: DeleteResult = await experiencia_collection.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f"Experiencia {id} no encontrada")