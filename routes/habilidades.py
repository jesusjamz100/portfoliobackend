from fastapi import APIRouter, Body, status, Depends
from config.jwthandler import get_current_user
from models.habilidades_model import HabilidadModel, UpdateHabilidadModel, HabilidadesCollection
from services.habilidades_service import HabilidadesService

router = APIRouter(
    prefix='/habilidades',
    tags=['habilidades']
)

service = HabilidadesService()

@router.get(
    '/',
    description="Obtener todas las habilidades",
    response_model=HabilidadesCollection,
    response_model_by_alias=False
)
async def all_habilidades():
    return await service.get_all_habilidades()

@router.get(
    '/{id}',
    description="Obtener una habilidad",
    response_model=HabilidadModel,
    response_model_by_alias=False
)
async def habilidad_by_id(id: str):
    return await service.get_habilidad_by_id(id)

@router.post(
    '/',
    description="Crear una habilidad",
    response_model=HabilidadModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def add_habilidad(habilidad: HabilidadModel = Body(...)):
    return await service.save_habilidad(habilidad)

@router.put(
    '/{id}',
    description="Actualizar una habilidad",
    response_model=HabilidadModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def update_habilidad(id: str, habilidad: UpdateHabilidadModel = Body(...)):
    return await service.update_habilidad(id, habilidad)

@router.delete('/{id}', description="Eliminar una habilidad", dependencies=[Depends(get_current_user)])
async def delete_habilidad(id: str):
    return await service.delete_habilidad(id)