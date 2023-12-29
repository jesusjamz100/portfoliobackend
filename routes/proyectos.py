from fastapi import APIRouter, Body, status, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import Response
from config.db import proyectos_collection
from config.jwthandler import get_current_user
from models.proyectosModel import ProyectoModel, ProyectosCollection, UpdateProyectoModel
from bson import ObjectId
from pymongo import ReturnDocument
from config.saveimages import saveimage
from typing import Annotated

router = APIRouter(
    prefix='/proyectos',
    tags=['proyectos']
)

@router.get(
    '/',
    description="Obtener todos los proyectos",
    response_model=ProyectosCollection,
    response_model_by_alias=False
)
async def allProyectos():
    return ProyectosCollection(proyectos=await proyectos_collection.find().to_list(1000))

@router.get(
    '/{id}',
    description="Obtener un proyecto",
    response_model=ProyectoModel,
    response_model_by_alias=False
)
async def mostrarProyecto(id: str):
    if (
        proyecto := await proyectos_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return proyecto
    raise HTTPException(status_code=404, detail=f'Proyecto {id} no encontrado')

@router.post(
    '/',
    description="Crear un nuevo proyecto",
    response_model=ProyectoModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def addProyecto(proyecto: ProyectoModel = Body(...)):
    new_proyecto = await proyectos_collection.insert_one(
        proyecto.model_dump(by_alias=True, exclude=["id"])
    )
    created_proyecto = await proyectos_collection.find_one(
        {"_id": new_proyecto.inserted_id}
    )
    return created_proyecto

@router.put(
    '/{id}',
    description="Actualizar un proyecto",
    response_model=ProyectoModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def updateProyecto(id: str, proyecto: UpdateProyectoModel = Body(...)):
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
    
    raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')

@router.delete('/{id}', description="Eliminar un proyecto", dependencies=[Depends(get_current_user)])
async def deleteProyecto(id: str):
    delete_result = await proyectos_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f'El proyecto {id} no existe')