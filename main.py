from fastapi import FastAPI, Body, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from routes import users, educacion, experiencia, idiomas, habilidades, proyectos
from models.mensajeModel import MensajeModel
from config.mail import send_email_async, send_email_background
from config.jwthandler import get_current_user

app = FastAPI(
    title="Curriculum"
)

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get('/user', dependencies=[Depends(get_current_user)])
async def checkAuth():
    return {'user': True}

@app.post(
    '/contacto/async',
    description='Contáctame por email asincrono',
    response_model_by_alias=False
)
async def contacto_async(mensaje: MensajeModel = Body(...)):
    return await send_email_async(mensaje.nombre, mensaje.email, mensaje.mensaje)

@app.post(
    '/contacto/background',
    description='Contactame por email background task',
    response_model_by_alias=False
)
def contacto_backgound(background_tasks: BackgroundTasks, mensaje: MensajeModel = Body(...)):
    return send_email_background(background_tasks, mensaje.nombre, mensaje.email, mensaje.mensaje)