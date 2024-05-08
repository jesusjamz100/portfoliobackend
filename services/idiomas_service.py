from fastapi import Response, HTTPException
from config.db import idiomas_collection
from repositories.idiomas_repository import IdiomasRepository
from models.idiomas_model import IdiomaModel, IdiomaCollection, UpdateIdiomaModel
from bson import ObjectId
from pymongo import ReturnDocument

class IdiomaService:

    def __init__(self) -> None:
        self.repository = IdiomasRepository()

    async def get_all_idiomas(self) -> IdiomaCollection:
        return await self.repository.get_all()
    
    async def get_idioma_by_id(self, id: str) -> IdiomaModel:
        return await self.repository.get_by_id(id)
    
    async def save_idioma(self, idioma: IdiomaModel) -> IdiomaModel:
        return await self.repository.save(idioma)
    
    async def delete_idioma(self, id: str) -> Response:
        return await self.repository.delete_by_id(id)
    
    async def update_idioma(self, id: str, idioma: UpdateIdiomaModel) -> IdiomaModel:
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