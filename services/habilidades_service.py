from fastapi import Response, HTTPException, status
from repositories.habilidades_repository import HabilidadesRepository
from models.habilidades_model import HabilidadModel, HabilidadesCollection, UpdateHabilidadModel
from pymongo.results import DeleteResult

class HabilidadesService:

    def __init__(self) -> None:
        self.repository = HabilidadesRepository()

    async def get_all_habilidades(self) -> HabilidadesCollection:
        return await self.repository.get_all()
    
    async def get_habilidad_by_id(self, id: str) -> HabilidadModel:
        habilidad = await self.repository.get_by_id(id)
        if habilidad:
            return habilidad
        raise HTTPException(status_code=404, detail=f"La habilidad con ID: {id} no se encuentra")
    
    async def save_habilidad(self, habilidad: HabilidadModel) -> HabilidadModel:
        return await self.repository.save(habilidad)

    async def delete_habilidad(self, id: str) -> Response:
        delete_result: DeleteResult = await self.repository.delete_by_id(id)
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f"Educacion {id} no encontrada")
    
    async def update_habilidad(self, id: str, habilidad: UpdateHabilidadModel) -> HabilidadModel:
        habilidad = {
            k: v for k, v in habilidad.model_dump(by_alias=True).items() if v is not None
        }

        if len(habilidad) >= 1:
            update_result = await self.repository.update_by_id(id, habilidad)
            if update_result is not None:
                return update_result
            else:
                HTTPException(status_code=404, detail=f'Habilidad {id} no encontrada')
        
        if (existing_habilidad := await self.repository.get_by_id(id)) is not None:
            return existing_habilidad
        
        raise HTTPException(status_code=404, detail=f'Habilidad {id} no encontrada')