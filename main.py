from fastapi import FastAPI, Body, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes import users, educacion, experiencia, idiomas, habilidades, proyectos
from models.mensaje_model import MensajeModel
from services.contact_service import contact_service
from services.jwt_service import jwt_service

app = FastAPI(
    title="Curriculum"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(educacion.router)
app.include_router(experiencia.router)
app.include_router(idiomas.router)
app.include_router(habilidades.router)
app.include_router(proyectos.router)

@app.get('/')
async def root():
    return {"message": "Bienvenido a mi curriculum"}

@app.get('/user', dependencies=[Depends(jwt_service.get_current_user)])
async def checkAuth():
    return {'user': True}

@app.post(
    '/contacto/async',
    description='Contáctame por email asincrono',
    response_model_by_alias=False
)
async def contacto_async(mensaje: MensajeModel = Body(...)):
    return await contact_service.send_email_async(mensaje.nombre, mensaje.email, mensaje.mensaje)

@app.post(
    '/contacto/background',
    description='Contactame por email background task',
    response_model_by_alias=False
)
def contacto_backgound(background_tasks: BackgroundTasks, mensaje: MensajeModel = Body(...)):
    return contact_service.send_email_background(background_tasks, mensaje.nombre, mensaje.email, mensaje.mensaje)