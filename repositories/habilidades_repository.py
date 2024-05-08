from fastapi import HTTPException, Response, status
from config.db import habilidades_collection
from models.habilidades_model import HabilidadModel, HabilidadesCollection
from bson import ObjectId
from pymongo.results import DeleteResult

class HabilidadesRepository:

    async def get_all(self) -> HabilidadesCollection:
        return HabilidadesCollection(habilidades=await habilidades_collection.find().to_list(1000))
    
    async def get_by_id(self, id: str) -> HabilidadModel:
        if (
            habilidad := await habilidades_collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return habilidad
        raise HTTPException(status_code=404, detail=f'La habilidad {id} no existe')
    
    async def save(self, habilidad: HabilidadModel) -> HabilidadModel:
        new_habilidad = await habilidades_collection.insert_one(
            habilidad.model_dump(by_alias=True, exclude=['id'])
        )
        created_habilidad = await habilidades_collection.find_one(
            {"_id": new_habilidad.inserted_id}
        )
        return created_habilidad
    
    async def delete_by_id(self, id: str):
        delete_result: DeleteResult = await habilidades_collection.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)