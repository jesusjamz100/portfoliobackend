from fastapi import APIRouter, Body, status, Depends
from services.jwt_service import jwt_service
from models.experiencia_model import ExperienciaModel, UpdateExperienciaModel, ExperienciaCollection
from services.experiencia_service import ExperienciaService

router = APIRouter(
    prefix='/experiencia',
    tags=['experiencia laboral']
)

service = ExperienciaService()

@router.get(
    '/',
    description="Toda la experiencia laboral",
    response_model=ExperienciaCollection,
    response_model_by_alias=False
)
async def all_experiencia():
    return await service.get_all_experiencia()

@router.get(
    '/{id}',
    description="Obtener una experiencia laboral",
    response_model=ExperienciaModel,
    response_model_by_alias=False
)
async def experiencia_by_id(id: str):
    return await service.get_experiencia_by_id(id)

@router.post(
    '/',
    description="Crear una experiencia laboral",
    response_model=ExperienciaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(jwt_service.get_current_user)]
)
async def add_experiencia(experiencia: ExperienciaModel = Body(...)):
    return await service.save_experiencia(experiencia)

@router.put(
    '/{id}',
    description="Actualizar una experiencia laboral",
    response_model=ExperienciaModel,
    response_model_by_alias=False,
    dependencies=[Depends(jwt_service.get_current_user)]
)
async def update_experiencia(id: str, experiencia: UpdateExperienciaModel = Body(...)):
    return await service.update_experiencia(id, experiencia)

@router.delete('/{id}', description="Eliminar una experiencia", dependencies=[Depends(jwt_service.get_current_user)])
async def delete_experiencia(id: str):
    return await service.delete_experiencia(id)