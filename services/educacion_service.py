from fastapi import Response, HTTPException, status
from repositories.educacion_repository import EducacionRepository
from models.educacion_model import EducacionCollection, EducacionModel, UpdateEducacionModel
from pymongo.results import DeleteResult

class EducacionService:
    
    def __init__(self) -> None:
        self.repository = EducacionRepository()

    async def get_all_educacion(self) -> EducacionCollection:
        return await self.repository.get_all()

    async def get_educacion_by_id(self, id: str) -> EducacionModel:
        educacion = await self.repository.get_by_id(id)
        if educacion:
            return educacion
        raise HTTPException(status_code=404, detail=f"La educacion con ID: {id} no se encuentra")

    async def save_educacion(self, educacion: EducacionModel) -> EducacionModel:
        return await self.repository.save(educacion)
    
    async def delete_educacion(self, id: str) -> Response:
        delete_result: DeleteResult = await self.repository.delete_by_id(id)
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")
    
    async def update_educacion(self, id: str, educacion: UpdateEducacionModel) -> EducacionModel:
        educacion = {
            k: v for k, v in educacion.model_dump(by_alias=True).items() if v is not None
        }

        if len(educacion) >= 1:
            update_result = await self.repository.update_by_id(id, educacion)
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=404, detail=f'Educacion {id} no fue encontrada')
            
        if (existing_educacion := await self.repository.get_by_id(id)) is not None:
            return existing_educacion
        
        raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")