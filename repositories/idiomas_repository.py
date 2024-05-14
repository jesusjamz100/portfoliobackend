from config.db import idiomas_collection
from models.idiomas_model import IdiomaModel, IdiomaCollection
from bson import ObjectId
from pymongo.results import DeleteResult
from pymongo import ReturnDocument

class IdiomasRepository:

    async def get_all(self) -> IdiomaCollection:
        return IdiomaCollection(idiomas=await idiomas_collection.find().to_list(1000))

    async def get_by_id(self, id: str) -> IdiomaModel:
        return await idiomas_collection.find_one({"_id": ObjectId(id)})
    
    async def save(self, idioma: IdiomaModel) -> IdiomaModel:
        new_idioma = await idiomas_collection.insert_one(
            idioma.model_dump(by_alias=True, exclude=["id"])
        )
        created_idioma = await idiomas_collection.find_one(
            {"_id": new_idioma.inserted_id}
        )
        return created_idioma

    async def delete_by_id(self, id: str) -> DeleteResult:
        return await idiomas_collection.delete_one({"_id": ObjectId(id)})
    
    async def update_by_id(self, id: str, idioma) -> IdiomaModel:
        return await idiomas_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": idioma},
                return_document=ReturnDocument.AFTER
            )