from datetime import datetime
from typing import Dict, Any

from src.database.db_config import db

class Sents(db.Model):
    __tablename__ = 'sents'
    
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Sent from {self.sender} to {self.recipient}>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'message': self.message,
            'sent_at': self.sent_at.isoformat()
        }