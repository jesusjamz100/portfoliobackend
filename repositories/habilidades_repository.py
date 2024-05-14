from config.db import habilidades_collection
from models.habilidades_model import HabilidadModel, HabilidadesCollection
from bson import ObjectId
from pymongo.results import DeleteResult
from pymongo import ReturnDocument

class HabilidadesRepository:

    async def get_all(self) -> HabilidadesCollection:
        return HabilidadesCollection(habilidades=await habilidades_collection.find().to_list(1000))
    
    async def get_by_id(self, id: str) -> HabilidadModel:
        return await habilidades_collection.find_one({"_id": ObjectId(id)})
    
    async def save(self, habilidad: HabilidadModel) -> HabilidadModel:
        new_habilidad = await habilidades_collection.insert_one(
            habilidad.model_dump(by_alias=True, exclude=['id'])
        )
        created_habilidad = await habilidades_collection.find_one(
            {"_id": new_habilidad.inserted_id}
        )
        return created_habilidad
    
    async def delete_by_id(self, id: str) -> DeleteResult:
        return await habilidades_collection.delete_one({"_id": ObjectId(id)})
    
    async def update_by_id(self, id: str, habilidad) -> HabilidadModel:
        return await habilidades_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": habilidad},
                return_document=ReturnDocument.AFTER
            )