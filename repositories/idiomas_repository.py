from fastapi import HTTPException, Response, status
from config.db import idiomas_collection
from models.idiomas_model import IdiomaModel, IdiomaCollection
from bson import ObjectId
from pymongo.results import DeleteResult


class IdiomasRepository:

    async def get_all(self) -> IdiomaCollection:
        return IdiomaCollection(idiomas=await idiomas_collection.find().to_list(1000))

    async def get_by_id(self, id: str) -> IdiomaModel:
        if (
            idioma := await idiomas_collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return idioma
        raise HTTPException(status_code=404, detail=f'El idioma {id} no fue encontrado')
    
    async def save(self, idioma: IdiomaModel) -> IdiomaModel:
        new_idioma = await idiomas_collection.insert_one(
            idioma.model_dump(by_alias=True, exclude=["id"])
        )
        created_idioma = await idiomas_collection.find_one(
            {"_id": new_idioma.inserted_id}
        )
        return created_idioma

    async def delete_by_id(self, id: str):
        delete_result: DeleteResult = await idiomas_collection.delete_one({"_id": ObjectId(id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')