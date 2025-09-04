from datetime import datetime
from typing import Dict, Any

from src.database.db_config import db

class Sents(db.Model):
    __tablename__ = 'sents'
    
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    contact = db.relationship('Contacts', backref='sents', lazy=True)

    def __repr__(self):
        return f'<Sent from {self.sender} to {self.recipient}>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'sender': self.sender,
            'contact': self.contact.to_dict(),
            'message': self.message,
            'sent_at': self.sent_at.isoformat()
        }