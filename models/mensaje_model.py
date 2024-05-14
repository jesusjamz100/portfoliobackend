from pydantic import BaseModel, Field, EmailStr, ConfigDict

class MensajeModel(BaseModel):
    nombre: str = Field(...)
    email: EmailStr = Field(...)
    mensaje: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nombre": "John Doe",
                "email": "correo@correo.com",
                "mensaje": "Me gustaria que hablaramos de un proyecto"
            }
        }
    )