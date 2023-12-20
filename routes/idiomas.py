from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import Response
from config.db import idiomas_collection
from config.jwthandler import get_current_user
from models.idiomasModel import IdiomaCollection, IdiomaModel, UpdateIdiomaModel
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter(
    prefix='/idiomas',
    tags=['idiomas']
)

@router.get(
    '/',
    description='Obtener todos los idiomas',
    response_model=IdiomaCollection,
    response_model_by_alias=False
)
async def allIdiomas():
    return IdiomaCollection(idiomas=await idiomas_collection.find().to_list(1000))

@router.get(
    '/{id}',
    description="Obtener un idioma",
    response_model=IdiomaModel,
    response_model_by_alias=False
)
async def mostrarIdioma(id: str):
    if (
        idioma := await idiomas_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return idioma
    raise HTTPException(status_code=404, detail=f'El idioma {id} no fue encontrado')

@router.post(
    '/',
    description="Crear un nuevo idioma",
    response_model=IdiomaModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def addIdioma(idioma: IdiomaModel = Body(...)):
    new_idioma = await idiomas_collection.insert_one(
        idioma.model_dump(by_alias=True, exclude=["id"])
    )
    created_idioma = await idiomas_collection.find_one(
        {"_id": new_idioma.inserted_id}
    )
    return created_idioma

@router.put(
    '/{id}',
    description="Actualizar un idioma",
    response_model=IdiomaModel,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_user)]
)
async def updateIdioma(id: str, idioma: UpdateIdiomaModel = Body(...)):
    idioma = {
        k: v for k, v in idioma.model_dump(by_alias=True).items() if v is not None
    }
    if len(idioma) >= 1:
        update_result = await idiomas_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": idioma},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')
        
    if (existing_idioma := await idiomas_collection.find_one({"_id": id})) is not None:
        return existing_idioma
    
    raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')

@router.delete('/{id}', description="Eliminar un idioma", dependencies=[Depends(get_current_user)])
async def deleteIdioma(id: str):
    delete_result = await idiomas_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')