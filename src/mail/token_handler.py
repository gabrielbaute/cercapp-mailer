import jwt
from typing import Optional, Union
from datetime import datetime, timedelta
from flask import current_app

from src.config import Config

class MailTokenHandler:
    def __init__(self, user_id: int):
        self.module_name = "MailTokenHandler"
        self.user_id = user_id

    def create_reset_token(self) -> str:
        """Genera un token JWT para recuperación de contraseña"""
        expiration = timedelta(minutes=Config.RESET_TOKEN_EXP_MINUTES)
        payload = {
            'user_id': self.user_id,
            'exp': datetime.utcnow() + expiration
        }
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        current_app.logger.debug(f"[{self.module_name}]: Token creado: {token}")
        return token

    @staticmethod
    def decode_token(token: str) -> Union[int, None]:
        """
        Decodifica el token y retorna el user_id si es válido.
        Retorna None si el token es inválido o ha expirado.

        :param token: Token JWT a decodificar
        :return: user_id o None
        """
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_app.logger.debug(f"[{MailTokenHandler.__name__}]: Token decodificado: {payload}")
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None