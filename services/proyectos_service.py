import json
from fastapi import Response, HTTPException, UploadFile
from config.db import proyectos_collection
from config.saveimages import convert_and_resize_image, upload_to_firebase
from repositories.proyectos_repository import ProyectoRepository
from models.proyectos_model import ProyectoModel, ProyectosCollection, UpdateProyectoModel
from bson import ObjectId
from pymongo import ReturnDocument
from pydantic import parse_obj_as

class ProyectoService:

    def __init__(self) -> None:
        self.repository = ProyectoRepository()

    async def get_all_proyectos(self) -> ProyectosCollection:
        return await self.repository.get_all()
    
    async def get_proyecto_by_id(self, id: str) -> ProyectoModel:
        return await self.repository.get_by_id(id)
    
    async def save_proyecto(self, proyecto: str, image: UploadFile) -> ProyectoModel:
        
        proyecto_dict = json.loads(proyecto)

        converted_img = convert_and_resize_image(await image.read())
        titulo = proyecto_dict['titulo']

        link = upload_to_firebase(converted_img, titulo)

        proyecto_dict['imgUrl'] = link

        proyecto_model = parse_obj_as(ProyectoModel, proyecto_dict)

        return await self.repository.save(proyecto_model)
    
    async def delete_proyecto(self, id: str) -> Response:
        return await self.repository.delete_by_id(id)
    
    async def update_proyecto(self, id: str, proyecto: UpdateProyectoModel) -> ProyectoModel:
        proyecto = {
            k: v for k, v in proyecto.model_dump(by_alias=True).items() if v is not None
        }
        if len(proyecto) >= 1:
            update_result = await proyectos_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": proyecto},
                return_document=ReturnDocument.AFTER
            )
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'El proyecto {id} no existe')
            
        if (existing_proyecto := await proyectos_collection.find_one({"_id": id})) is not None:
            return existing_proyecto
        
        raise HTTPException(status_code=404, detail=f'El proyecto {id} no existe')