import logging
from typing import Optional, List
from flask import current_app

from src.database.models import Sents
from src.controllers.database_controller import DatabaseController
from src.schemas import SentCreate, SentResponse
from src.errors import NotFoundError

class SentController(DatabaseController):
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user
        self.controller_name = "SentController"
        self.logger = logging.getLogger(f"[{self.controller_name}]")
        self.logger.info(f"{self.controller_name} inicializado.")
    
    # Métodos para crear
    def register_sent(self, data: SentCreate) -> Optional[SentResponse]:
        """Create a new sent."""
        sent = Sents(
            sender=data.sender,
            contact_id=data.contact_id,
            message=data.message
        )
        
        self.logger.debug(f"Creando nuevo enviado: {data.contact_id}")
        self.db.session.add(sent)
        self._commit_or_rollback()
        return self._to_response(sent, SentResponse)

    # Métodos para leer
    def get_sent_by_id(self, sent_id: int) -> Optional[SentResponse]:
        """Get a sent by id."""
        sent = self.session.get(Sents, sent_id)
        if not sent:
            raise NotFoundError(f"Enviado con id {sent_id} no encontrado")
        self.logger.debug(f"Obteniendo enviado por id: {sent_id}")
        return self._to_response(sent, SentResponse)
    
    def get_all_sents(self) -> List[SentResponse]:
        """Get all sents."""
        sents = self.session.query(Sents).all()
        self.logger.debug("Obteniendo todos los enviados")
        return [self._to_response(sent, SentResponse) for sent in sents]
    
    def get_sents_by_contact_id(self, contact_id: int) -> List[SentResponse]:
        """Get sents by contact id."""
        sents = self.session.query(Sents).filter_by(contact_id=contact_id).all()
        self.logger.debug(f"Obteniendo enviados por id de contacto: {contact_id}")
        return [self._to_response(sent, SentResponse) for sent in sents]
    
    def get_sents_by_sender(self, sender: str) -> List[SentResponse]:
        """Get sents by sender."""
        sents = self.session.query(Sents).filter_by(sender=sender).all()
        self.logger.debug(f"Obteniendo enviados por remitente: {sender}")
        return [self._to_response(sent, SentResponse) for sent in sents]
    
    def get_sents_by_date(self, date: str) -> List[SentResponse]:
        """Get sents by date."""
        sents = self.session.query(Sents).filter_by(sent_at=date).all()
        self.logger.debug(f"Obteniendo enviados por fecha: {date}")
        return [self._to_response(sent, SentResponse) for sent in sents]
    
    def get_sents_by_range(self, start_date: str, end_date: str) -> List[SentResponse]:
        """Get sents by date range."""
        sents = self.session.query(Sents).filter(Sents.sent_at.between(start_date, end_date)).all()
        self.logger.debug(f"Obteniendo enviados entre fechas: {start_date} y {end_date}")
        return [self._to_response(sent, SentResponse) for sent in sents]