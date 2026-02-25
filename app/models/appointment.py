from app.database import db
from app.models.base_model import BaseModel
from .patient import Patient
from .doctor import Doctor

class Appointment(BaseModel):
    __tablename__ = 'appointments'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='scheduled')
    patient = db.relationship('Patient', backref=db.backref('appointments'))
    doctor = db.relationship('Doctor', backref=db.backref('appointments'))

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date.isoformat(),
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }