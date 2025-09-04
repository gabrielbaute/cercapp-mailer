import logging
from typing import Optional, List
from flask import current_app
from werkzeug.security import generate_password_hash

from src.database.models import Users
from src.controllers.database_controller import DatabaseController
from src.schemas import UserCreate, UserResponse, UserUpdate
from src.errors import NotFoundError

class UsersController(DatabaseController):
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user
        self.controller_name = "UsersController"
        self.logger = logging.getLogger(self.controller_name)
        self.logger.info(f"{self.controller_name} inicializado.")
    
    def _get_user_instance_by_id(self, user_id: int) -> Optional[Users]:
        """Get a user instance by id."""
        try:
            user = Users.query.get(user_id)
            self.logger.debug(f"Obteniendo usuario por id: {user_id}")
        except Exception as e:
            self.logger.error(f"Error al obtener el usuario: {e}")
            return None
        return user

    def get_user_instance_by_email(self, email: str) -> Optional[Users]:
        """Retorna la instancia ORM del usuario por email."""
        try:
            user = Users.query.filter_by(email=email).first()
            self.logger.debug(f"Obteniendo usuario por email: {email}")
        except Exception as e:
            self.logger.error(f"Error al obtener el usuario: {e}")
            return None
        return user

    def create_user(self, data: UserCreate) -> Optional[UserResponse]:
        """Create a new user."""
        existing = Users.query.filter(
            (Users.username == data.username) | (Users.email == data.email)
        ).first()
        if existing:
            raise ValueError("Usuario o email ya registrados")

        user = Users(
            username=data.username,
            password_hash=generate_password_hash(data.password),
            email=data.email
        )
        
        self.db.session.add(user)
        self.logger.info(f"Creando nuevo usuario: {data.username}")
        self._commit_or_rollback()
        return self._to_response(user, UserResponse)
    
    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """Get a user by username."""
        user = Users.query.filter_by(username=username).first()
        self.logger.debug(f"Obteniendo usuario por username: {username}")
        return self._to_response(user, UserResponse)
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email."""
        user =  Users.query.filter_by(email=email).first()
        self.logger.debug(f"Obteniendo usuario por email: {email}")
        return self._to_response(user, UserResponse)
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get a user by id."""
        
        user = self._get_user_instance_by_id(id)
        if not user:
            raise NotFoundError(f"[{self.controller_name}]: Usuario con id {user_id} no encontrado")
        
        self.logger.debug(f"Obteniendo usuario por id: {user_id}")
        return self._to_response(user, UserResponse)
    
    def get_all_users(self) -> List[UserResponse]:
        """Get all users."""
        users = Users.query.all()
        self.logger.debug(f"Obteniendo una lista de todos los usuarios")
        return [self._to_response(user, UserResponse) for user in users]
    
    def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserResponse]:
        """Update a user."""
        
        user = self._get_user_instance_by_id(user_id)
        if not user:
            raise NotFoundError(f"[{self.controller_name}]: Usuario con id {user_id} no encontrado")
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        
        self.logger.debug(f"Actualizando usuario con id: {user_id}")
        self._commit_or_rollback()
        return self._to_response(user, UserResponse)
    
    def update_user_password(self, user_id: int, password: str) -> Optional[bool]:
        """Update a user password."""
        
        user = self._get_user_instance_by_id(user_id)
        if not user:
            raise NotFoundError(f"[{self.controller_name}]: Usuario con id {user_id} no encontrado")
        
        user.password_hash = generate_password_hash(password)
        self.logger.debug(f"Actualizando contraseña del usuario con id: {user_id}")
        self._commit_or_rollback()
        return True
    
    def delete_user(self, user_id: int) -> Optional[bool]:
        """Delete a user."""
        
        user = self._get_user_instance_by_id(user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {user_id} no encontrado")
        
        self.logger.info(f"Eliminando usuario: {user.username} con id: {user_id}")
        self.session.delete(user)
        self._commit_or_rollback()
        return True