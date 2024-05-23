from fastapi import APIRouter, Body, status, Depends, UploadFile, File, Form
from services.proyectos_service import ProyectoService
from services.jwt_service import jwt_service
from models.proyectos_model import ProyectoModel, ProyectosCollection, UpdateProyectoModel
from typing import Optional

router = APIRouter(
    prefix='/proyectos',
    tags=['proyectos']
)

service = ProyectoService()

@router.get(
    '/',
    description="Obtener todos los proyectos",
    response_model=ProyectosCollection,
    response_model_by_alias=False
)
async def all_proyectos():
    return await service.get_all_proyectos()

@router.get(
    '/{id}',
    description="Obtener un proyecto",
    response_model=ProyectoModel,
    response_model_by_alias=False
)
async def proyecto_by_id(id: str):
    return await service.get_proyecto_by_id(id)

@router.post(
    '/',
    description="Crear un nuevo proyecto",
    response_model=ProyectoModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(jwt_service.get_current_user)]
)
async def add_proyecto(proyecto: str = Form(...), image: UploadFile = File(...)):
    return await service.save_proyecto(proyecto, image)

@router.put(
    '/{id}',
    description="Actualizar un proyecto",
    response_model=ProyectoModel,
    response_model_by_alias=False,
    dependencies=[Depends(jwt_service.get_current_user)]
)
async def update_proyecto(id: str, proyecto: str = Form(...), image: UploadFile = File(None)):
    return await service.update_proyecto(id, proyecto, image)

@router.delete('/{id}', description="Eliminar un proyecto", dependencies=[Depends(jwt_service.get_current_user)])
async def delete_proyecto(id: str):
    return await service.delete_proyecto(id)