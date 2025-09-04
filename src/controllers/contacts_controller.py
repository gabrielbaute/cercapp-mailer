import logging
from typing import Optional, List, Union, Any
from flask import current_app

from src.database.models import Contacts
from src.controllers.database_controller import DatabaseController
from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.errors import NotFoundError

class ContactsController(DatabaseController):
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user
        self.controller_name = "ContactsController"
        self.logger = logging.getLogger(f"[{self.controller_name}]")
        self.logger.info(f"{self.controller_name} inicializado.")
    
    # Métodos para crear
    def create_contact(self, data: ContactCreate) -> Optional[ContactResponse]:
        """Create a new contact."""
        contact = Contacts(
            username=data.username,
            email=data.email,
        )
        
        self.logger.debug(f"Creando nuevo contacto: {data.email}")
        self.db.session.add(contact)
        self._commit_or_rollback()
        return self._to_response(contact, ContactResponse)
    
    # Métodos para obtener
    def get_contact_by_id(self, contact_id: int) -> Optional[ContactResponse]:
        """Get a contact by id."""
        contact = self.session.get(Contacts, contact_id)
        if not contact:
            raise NotFoundError(f"Contacto con id {contact_id} no encontrado")
        self.logger.debug(f"Obteniendo contacto por id: {contact_id}")
        return self._to_response(contact, ContactResponse)
    
    def get_contacts_email(self, email: str) -> List[ContactResponse]:
        """Get contacts by email."""
        contacts = Contacts.query.filter_by(email=email).all()
        self.logger.debug(f"Obteniendo contactos por email: {email}")
        return [self._to_response(contact, ContactResponse) for contact in contacts]
    
    def get_all_contacts(self) -> List[ContactResponse]:
        """Get all contacts."""
        contacts = Contacts.query.all()
        self.logger.debug(f"Obteniendo todos los contactos")
        return [self._to_response(contact, ContactResponse) for contact in contacts]
    
    # Métodos para actualizar
    def update_contact(self, contact_id: int, data: ContactUpdate) -> Optional[ContactResponse]:
        """Update a contact."""
        contact = self.session.get(Contacts, contact_id)
        if not contact:
            raise NotFoundError(f"Contacto con id {contact_id} no encontrado")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)
        self.logger.debug(f"Actualizando contacto con id: {contact_id}")
        self._commit_or_rollback()
        return self._to_response(contact, ContactResponse)
    
    # Métodos para eliminar
    def delete_contact(self, contact_id: int) -> Optional[bool]:
        """Delete a contact."""
        contact = self.session.get(Contacts, contact_id)
        if not contact:
            raise NotFoundError(f"Contacto con id {contact_id} no encontrado")
        
        self.logger.info(f"Eliminando contacto: {contact.email} con id: {contact_id}")
        self.session.delete(contact)
        self._commit_or_rollback()
        return True