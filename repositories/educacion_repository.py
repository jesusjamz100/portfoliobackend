from fastapi import HTTPException, Response, status
from config.db import educacion_collection
from models.educacion_model import EducacionCollection, EducacionModel
from bson import ObjectId
from pymongo.results import DeleteResult

class EducacionRepository:

    async def get_all(self) -> EducacionCollection:
        return EducacionCollection(educacion=await educacion_collection.find().to_list(1000))

    async def get_by_id(self, id: str) -> EducacionModel:
        if (
            educacion := await educacion_collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return educacion
        raise HTTPException(status_code=404, detail=f"La educacion con ID: {id} no se encuentra")
    
    async def save(self, educacion: EducacionModel) -> EducacionModel:
        new_educacion = await educacion_collection.insert_one(
            educacion.model_dump(by_alias=True, exclude=["id"])
        )
        created_educacion = await educacion_collection.find_one(
            {"_id": new_educacion.inserted_id}
        )
        return created_educacion
    
    async def delete_by_id(self, id: str):
        delete_result: DeleteResult = await educacion_collection.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")