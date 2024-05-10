from fastapi import HTTPException, Response, status
from config.db import proyectos_collection
from models.proyectos_model import ProyectoModel, ProyectosCollection
from bson import ObjectId
from pymongo.results import DeleteResult

class ProyectoRepository:

    async def get_all(self) -> ProyectosCollection:
        return ProyectosCollection(proyectos=await proyectos_collection.find().to_list(1000))
    
    async def get_by_id(self, id: str) -> ProyectoModel:
        if (
            proyecto := await proyectos_collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return proyecto
        raise HTTPException(status_code=404, detail=f'Proyecto {id} no encontrado')
    
    async def save(self, proyecto: ProyectoModel) -> ProyectoModel:

        new_proyecto = await proyectos_collection.insert_one(
            proyecto.model_dump(by_alias=True, exclude=["id"])
        )
        created_proyecto = await proyectos_collection.find_one(
            {"_id": new_proyecto.inserted_id}
        )
        return created_proyecto
    
    async def delete_by_id(self, id: str):
        delete_result: DeleteResult = await proyectos_collection.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f'El proyecto {id} no existe')