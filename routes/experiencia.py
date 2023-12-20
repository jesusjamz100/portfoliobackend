from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import Response
from config.db import experiencia_collection
from config.jwthandler import get_current_user
from models.experienciaModel import ExperienciaModel, UpdateExperienciaModel, ExperienciaCollection
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter(
    prefix='/experiencia',
    tags=['experiencia laboral']
)

@router.get(
    '/',
    description="Toda la experiencia laboral",
    response_model=ExperienciaCollection,
    response_model_by_alias=False
)
async def allExperiencia():
    return ExperienciaCollection(experiencia=await experiencia_collection.find().to_list(1000))

@router.get(
    '/{id}',
    description="Obtener una experiencia laboral",
    response_model=ExperienciaModel,
    response_model_by_alias=False
)
async def mostrarExperiencia(id: str):
    if (
        experiencia := await experiencia_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return experiencia
    raise HTTPException(status_code=404, detail=f"La experiencia con ID: {id} no se encuentra")

@router.post(
    '/',
    description="Crear una experiencia laboral",
    response_model=ExperienciaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def addExperiencia(experiencia: ExperienciaModel = Body(...)):
    new_experiencia = await experiencia_collection.insert_one(
        experiencia.model_dump(by_alias=True, exclude=["id"])
    )
    created_experiencia = await experiencia_collection.find_one(
        {"_id": new_experiencia.inserted_id}
    )
    return created_experiencia

@router.put(
    '/{id}',
    description="Actualizar una experiencia laboral",
    response_model=ExperienciaModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def updateExperiencia(id: str, experiencia: UpdateExperienciaModel = Body(...)):
    experiencia = {
        k: v for k, v in experiencia.model_dump(by_alias=True).items() if v is not None
    }
    if len(experiencia) >= 1:
        update_result = await experiencia_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": experiencia},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f'Experiencia {id} no encontrada')
    
    if (existing_experiencia := await experiencia_collection.find_one({"_id": id}))  is not None:
        return existing_experiencia
    
    raise HTTPException(status_code=404, detail=f"Experiencia {id} no encontrada")

@router.delete('/{id}', description="Eliminar una experiencia", dependencies=[Depends(get_current_user)])
async def deleteExperiencia(id: str):
    delete_result = await experiencia_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Experiencia {id} no encontrada")