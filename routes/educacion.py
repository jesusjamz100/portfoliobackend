from fastapi import APIRouter, Body, status, Depends
from config.jwthandler import get_current_user
from models.educacion_model import EducacionModel, EducacionCollection, UpdateEducacionModel
from services.educacion_service import EducacionService

router = APIRouter(
    prefix='/educacion',
    tags=['educacion']
)

service = EducacionService()

@router.get(
    '/',
    description="Lista de toda la educacion",
    response_model=EducacionCollection,
    response_model_by_alias=False
)
async def all_educacion():
    return await service.get_all_educacion()

@router.get(
    '/{id}',
    description="Obtener una sola experiencia educativa",
    response_model=EducacionModel,
    response_model_by_alias=False
)
async def educacion_by_id(id: str):
    return await service.get_educacion_by_id(id)

@router.post(
    '/',
    description="Add educacion",
    response_model=EducacionModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def add_educacion(educacion: EducacionModel = Body(...)):
    return await service.save_educacion(educacion)

@router.put(
    '/{id}',
    description="Actualizar educacion",
    response_model=EducacionModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def update_educacion(id: str, educacion: UpdateEducacionModel = Body(...)):
    return await service.update_educacion(id, educacion)

@router.delete('/{id}', description="Eliminar educacion", dependencies=[Depends(get_current_user)])
async def delete_educacion(id: str):
    return await service.delete_educacion(id)