import json
from fastapi import Response, HTTPException, UploadFile
from services.images_service import images_service
from repositories.proyectos_repository import ProyectoRepository
from models.proyectos_model import ProyectoModel, ProyectosCollection, UpdateProyectoModel
from pydantic import parse_obj_as
from typing import Optional

class ProyectoService:

    def __init__(self) -> None:
        self.repository = ProyectoRepository()

    async def get_all_proyectos(self) -> ProyectosCollection:
        return await self.repository.get_all()
    
    async def get_proyecto_by_id(self, id: str) -> ProyectoModel:
        return await self.repository.get_by_id(id)
    
    async def save_proyecto(self, proyecto: str, image: UploadFile) -> ProyectoModel:
        
        proyecto_dict = json.loads(proyecto)

        converted_img = images_service.convert_and_resize_image(await image.read())
        titulo = proyecto_dict['titulo']

        link = images_service.upload_to_firebase(converted_img, titulo)

        proyecto_dict['imgUrl'] = link

        proyecto_model = parse_obj_as(ProyectoModel, proyecto_dict)

        return await self.repository.save(proyecto_model)
    
    async def delete_proyecto(self, id: str) -> Response:
        return await self.repository.delete_by_id(id)
    
    async def update_proyecto(self, id: str, proyecto: UpdateProyectoModel, image: Optional[UploadFile]) -> ProyectoModel:
        proyecto = {
            k: v for k, v in proyecto.model_dump(by_alias=True).items() if v is not None
        }
        if image:
            converted_img = images_service.convert_and_resize_image(await image.read())
            titulo = proyecto.titulo
            link = images_service.upload_to_firebase(converted_img, titulo)
            proyecto['imgUrl'] = link

        if len(proyecto) >= 1:
            update_result = await self.repository.update_by_id(id, proyecto)
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'El proyecto {id} no existe')
            
        if (existing_proyecto := await self.repository.get_by_id(id)) is not None:
            return existing_proyecto
        
        raise HTTPException(status_code=404, detail=f'El proyecto {id} no existe')