from config.db import experiencia_collection
from models.experiencia_model import ExperienciaModel, ExperienciaCollection
from bson import ObjectId
from pymongo.results import DeleteResult
from pymongo import ReturnDocument

class ExperienciaRepository:

    async def get_all(self) -> ExperienciaCollection:
        return ExperienciaCollection(experiencia=await experiencia_collection.find().to_list(1000))
    
    async def get_by_id(self, id: str) -> ExperienciaModel:
        return await experiencia_collection.find_one({"_id": ObjectId(id)})
        
    
    async def save(self, experiencia: ExperienciaModel) -> ExperienciaModel:
        new_experiencia = await experiencia_collection.insert_one(
            experiencia.model_dump(by_alias=True, exclude=["id"])
        )
        created_experiencia = await experiencia_collection.find_one(
            {"_id": new_experiencia.inserted_id}
        )
        return created_experiencia
    
    async def delete_by_id(self, id: str) ->  DeleteResult:
        return await experiencia_collection.delete_one({"_id": ObjectId(id)})
    
    async def update_by_id(self, id: str, experiencia) -> ExperienciaModel:
        return await experiencia_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": experiencia},
            return_document=ReturnDocument.AFTER
        )