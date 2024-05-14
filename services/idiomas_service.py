from fastapi import Response, HTTPException, status
from repositories.idiomas_repository import IdiomasRepository
from models.idiomas_model import IdiomaModel, IdiomaCollection, UpdateIdiomaModel
from pymongo.results import DeleteResult

class IdiomaService:

    def __init__(self) -> None:
        self.repository = IdiomasRepository()

    async def get_all_idiomas(self) -> IdiomaCollection:
        return await self.repository.get_all()
    
    async def get_idioma_by_id(self, id: str) -> IdiomaModel:
        idioma = await self.repository.get_by_id(id)
        if idioma:
            return idioma
        raise HTTPException(status_code=404, detail=f"El idioma con ID: {id} no se encuentra")
    
    async def save_idioma(self, idioma: IdiomaModel) -> IdiomaModel:
        return await self.repository.save(idioma)
    
    async def delete_idioma(self, id: str) -> Response:
        delete_result: DeleteResult = await self.repository.delete_by_id(id)
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f"Idioma {id} no encontrado")
    
    async def update_idioma(self, id: str, idioma: UpdateIdiomaModel) -> IdiomaModel:
        idioma = {
            k: v for k, v in idioma.model_dump(by_alias=True).items() if v is not None
        }
        
        if len(idioma) >= 1:
            update_result = await self.repository.update_by_id(id, idioma)
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')
            
        if (existing_idioma := await self.repository.get_by_id(id)) is not None:
            return existing_idioma
        
        raise HTTPException(status_code=404, detail=f'El idioma {id} no existe')