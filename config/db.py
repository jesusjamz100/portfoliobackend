import os
from motor import motor_asyncio
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

client = motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client.get_database("curriculum")

users_collection = db.get_collection("users")

educacion_collection = db.get_collection("educacion")
experiencia_collection = db.get_collection("experiencia")
idiomas_collection = db.get_collection("idiomas")
habilidades_collection = db.get_collection("habilidades")
proyectos_collection = db.get_collection("proyectos")

PyObjectId = Annotated[str, BeforeValidator(str)]