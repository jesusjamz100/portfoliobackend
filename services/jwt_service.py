import os
from typing_extensions import Annotated
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

class JWTService:
    
    oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')
    
    def __init__(self) -> None:
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.ALGORITHM = 'HS256'

    def create_access_token(self, username: str, expires_delta: timedelta):
        encode = {'sub': username}
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario')
            
            return {'username': username}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se pudo validar el usuario')
        
jwt_service = JWTService()