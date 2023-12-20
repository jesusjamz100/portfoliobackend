from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import Response
from models.habilidadesModel import HabilidadModel, UpdateHabilidadModel, HabilidadesCollection
from config.db import habilidades_collection
from config.jwthandler import get_current_user
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter(
    prefix='/habilidades',
    tags=['habilidades']
)

@router.get(
    '/',
    description="Obtener todas las habilidades",
    response_model=HabilidadesCollection,
    response_model_by_alias=False
)
async def allHabilidades():
    return HabilidadesCollection(habilidades=await habilidades_collection.find().to_list(1000))

@router.get(
    '/{id}',
    description="Obtener una habilidad",
    response_model=HabilidadModel,
    response_model_by_alias=False
)
async def mostrarHabilidad(id: str):
    if (
        habilidad := await habilidades_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return habilidad
    raise HTTPException(status_code=404, detail=f'La habilidad {id} no existe')

@router.post(
    '/',
    description="Crear una habilidad",
    response_model=HabilidadModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def addHabilidad(habilidad: HabilidadModel = Body(...)):
    new_habilidad = await habilidades_collection.insert_one(
        habilidad.model_dump(by_alias=True, exclude=['id'])
    )
    created_habilidad = await habilidades_collection.find_one(
        {"_id": new_habilidad.inserted_id}
    )
    return created_habilidad

@router.put(
    '/{id}',
    description="Actualizar una habilidad",
    response_model=HabilidadModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def updateHabilidad(id: str, habilidad: UpdateHabilidadModel = Body(...)):
    habilidad = {
        k: v for k, v in habilidad.model_dump(by_alias=True).items() if v is not None
    }

    if len(habilidad) >= 1:
        update_result = await habilidades_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": habilidad},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            HTTPException(status_code=404, detail=f'Habilidad {id} no encontrada')
    
    if (existing_habilidad := await habilidades_collection.find_one({"_id": id})) is not None:
        return existing_habilidad
    
    raise HTTPException(status_code=404, detail=f'Habilidad {id} no encontrada')

@router.delete('/{id}', description="Eliminar una habilidad", dependencies=[Depends(get_current_user)])
async def deleteHabilidad(id: str):
    delete_result = await habilidades_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)