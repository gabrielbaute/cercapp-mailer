from datetime import datetime
from typing import Dict

from src.database.db_config import db

class Contacts(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    #sents = db.relationship('Sents', backref='contact', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>: {self.email}'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }