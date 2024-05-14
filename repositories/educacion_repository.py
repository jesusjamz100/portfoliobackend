from config.db import educacion_collection
from models.educacion_model import EducacionCollection, EducacionModel
from bson import ObjectId
from pymongo.results import DeleteResult
from pymongo import ReturnDocument

class EducacionRepository:

    async def get_all(self) -> EducacionCollection:
        return EducacionCollection(educacion=await educacion_collection.find().to_list(1000))

    async def get_by_id(self, id: str) -> EducacionModel:
        return await educacion_collection.find_one({"_id": ObjectId(id)})
    
    async def save(self, educacion: EducacionModel) -> EducacionModel:
        new_educacion = await educacion_collection.insert_one(
            educacion.model_dump(by_alias=True, exclude=["id"])
        )
        created_educacion = await educacion_collection.find_one(
            {"_id": new_educacion.inserted_id}
        )
        return created_educacion
    
    async def delete_by_id(self, id: str) -> DeleteResult:
        return await educacion_collection.delete_one({"_id": ObjectId(id)})
    
    async def update_by_id(self, id: str, educacion) -> EducacionModel:
        return await educacion_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": educacion},
                return_document=ReturnDocument.AFTER
            )