from fastapi import APIRouter, Body, status, Depends
from services.jwt_service import jwt_service
from models.idiomas_model import IdiomaCollection, IdiomaModel, UpdateIdiomaModel
from services.idiomas_service import IdiomaService

router = APIRouter(
    prefix='/idiomas',
    tags=['idiomas']
)

service = IdiomaService()

@router.get(
    '/',
    description='Obtener todos los idiomas',
    response_model=IdiomaCollection,
    response_model_by_alias=False
)
async def all_idiomas():
    return await service.get_all_idiomas()

@router.get(
    '/{id}',
    description="Obtener un idioma",
    response_model=IdiomaModel,
    response_model_by_alias=False
)
async def idioma_by_id(id: str):
    return await service.get_idioma_by_id(id)

@router.post(
    '/',
    description="Crear un nuevo idioma",
    response_model=IdiomaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(jwt_service.get_current_user)]
)
async def add_idioma(idioma: IdiomaModel = Body(...)):
    return await service.save_idioma(idioma)

@router.put(
    '/{id}',
    description="Actualizar un idioma",
    response_model=IdiomaModel,
    response_model_by_alias=False,
    dependencies=[Depends(jwt_service.get_current_user)]
)
async def update_idioma(id: str, idioma: UpdateIdiomaModel = Body(...)):
    return await service.update_idioma(id, idioma)

@router.delete('/{id}', description="Eliminar un idioma", dependencies=[Depends(jwt_service.get_current_user)])
async def delete_idioma(id: str):
    return await service.delete_idioma(id)