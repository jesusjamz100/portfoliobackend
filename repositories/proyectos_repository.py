from config.db import proyectos_collection
from models.proyectos_model import ProyectoModel, ProyectosCollection
from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.results import DeleteResult

class ProyectoRepository:

    async def get_all(self) -> ProyectosCollection:
        return ProyectosCollection(proyectos=await proyectos_collection.find().to_list(1000))
    
    async def get_by_id(self, id: str) -> ProyectoModel:
        return await proyectos_collection.find_one({"_id": ObjectId(id)})
    
    async def save(self, proyecto: ProyectoModel) -> ProyectoModel:
        new_proyecto = await proyectos_collection.insert_one(
            proyecto.model_dump(by_alias=True, exclude=["id"])
        )
        created_proyecto = await proyectos_collection.find_one(
            {"_id": new_proyecto.inserted_id}
        )
        return created_proyecto
    
    async def delete_by_id(self, id: str) ->  DeleteResult:
        return await proyectos_collection.delete_one({"_id": ObjectId(id)})
    
    async def update_by_id(self, id: str, proyecto) -> ProyectoModel:
        return await proyectos_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": proyecto},
            return_document=ReturnDocument.AFTER
        )