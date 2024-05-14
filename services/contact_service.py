import os
from fastapi import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

class Envs:
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_FROM = os.environ.get('MAIL_FROM')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_FROM_NAME = os.environ.get('MAIL_FROM_NAME')

class ContactService:

    def __init__(self) -> None:
        self.conf = ConnectionConfig(
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

    async def send_email_async(self, nombre: str, email: str, mensaje: str):
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

        fm = FastMail(self.conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"msg": "El mensaje ha sido enviado"})

    async def send_email_background(self, background_tasks: BackgroundTasks, nombre: str, email: str, mensaje: str):
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

        fm = FastMail(self.conf)
        background_tasks.add_task(fm.send_message, message)
        return JSONResponse(status_code=200, content={"msg": "El mensaje ha sido enviado"})
    
contact_service = ContactService()