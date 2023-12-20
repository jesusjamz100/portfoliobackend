from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import Response
from config.db import educacion_collection
from config.jwthandler import get_current_user
from models.educacionModel import EducacionModel, EducacionCollection, UpdateEducacionModel
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter(
    prefix='/educacion',
    tags=['educacion']
)

@router.get(
    '/',
    description="Lista de toda la educacion",
    response_model=EducacionCollection,
    response_model_by_alias=False
)
async def allEducacion():
    return EducacionCollection(educacion=await educacion_collection.find().to_list(1000))

@router.get(
    '/{id}',
    description="Obtener una sola experiencia educativa",
    response_model=EducacionModel,
    response_model_by_alias=False
)
async def mostrarEducacion(id: str):
    if (
        educacion := await educacion_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return educacion
    raise HTTPException(status_code=404, detail=f"La educacion con ID: {id} no se encuentra")

@router.post(
    '/',
    description="Add educacion",
    response_model=EducacionModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def addEducacion(educacion: EducacionModel = Body(...)):
    new_educacion = await educacion_collection.insert_one(
        educacion.model_dump(by_alias=True, exclude=["id"])
    )
    created_educacion = await educacion_collection.find_one(
        {"_id": new_educacion.inserted_id}
    )
    return created_educacion

@router.put(
    '/{id}',
    description="Actualizar educacion",
    response_model=EducacionModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def updateEducacion(id: str, educacion: UpdateEducacionModel = Body(...)):
    educacion = {
        k: v for k, v in educacion.model_dump(by_alias=True).items() if v is not None
    }

    if len(educacion) >= 1:
        update_result = await educacion_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": educacion},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f'Educacion {id} no fue encontrada')
    
    if (existing_educacion := await educacion_collection.find_one({"_id": id})) is not None:
        return existing_educacion
    
    raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")

@router.delete('/{id}', description="Eliminar educacion", dependencies=[Depends(get_current_user)])
async def deleteEducacion(id: str):
    delete_result = await educacion_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")