import os
from dotenv import load_dotenv
from fastapi import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

load_dotenv()

class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')

conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email_async(nombre: str, email: str, mensaje: str):
    html = f"""
        <p>Nombre: {nombre}</p>
        <p>Email: {email}</p>
        <p>Mensaje: {mensaje}</p>
    """

    to: EmailStr = Envs.MAIL_USERNAME

    message = MessageSchema(
        subject="Nuevo mensaje del Portafolio",
        recipients=[to],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"msg": "El mensaje ha sido enviado"})

async def send_email_background(background_tasks: BackgroundTasks, nombre: str, email: str, mensaje: str):
    html = f"""
        <p>Nombre: {nombre}</p>
        <p>Email: {email}</p>
        <p>Mensaje: {mensaje}</p>
    """

    to: EmailStr = Envs.MAIL_USERNAME

    message = MessageSchema(
        subject="Nuevo mensaje del Portafolio",
        recipients=[to],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(status_code=200, content={"msg": "El mensaje ha sido enviado"})