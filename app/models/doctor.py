from app.database import db
from .base_model import BaseModel

class Doctor(BaseModel):
    __tablename__ = 'doctors'
    
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'email': self.email,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }