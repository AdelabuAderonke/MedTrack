from flask_restx import Namespace, fields
from app.database import db
from app.models.doctor import Doctor
from .base_resource import BaseResource

ns = Namespace("doctors", description="Doctor operations")

doctor_model = ns.model("Doctor", {
    "name":      fields.String(required=True, example="Dr. John Smith"),
    "email":          fields.String(required=True, example="john@hospital.com"),
    "gender":         fields.String(example="Male"),
    "specialization": fields.String(required=True, example="Cardiology"),
    "phone":          fields.String(example="07700900001"),
})

@ns.route("/")
class DoctorList(BaseResource):

    def get(self):
        """Get all doctors"""
        try:
            doctors = Doctor.query.all()
            return [d.to_dict() for d in doctors], 200
        except Exception as e:
            return self.handle_server_error(e)

    @ns.expect(doctor_model, validate=True)
    def post(self):
        """Register a new doctor"""
        try:
            data = ns.payload
            existing = Doctor.query.filter_by(email=data["email"]).first()
            if existing:
                return self.handle_conflict("A doctor with this email already exists")
            doctor = Doctor(**data)
            db.session.add(doctor)
            db.session.commit()
            return doctor.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)

@ns.route("/<int:id>")
class DoctorDetail(BaseResource):

    def get(self, id):
        """Get a doctor by ID"""
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return self.handle_not_found("Doctor", id)
            return doctor.to_dict(), 200
        except Exception as e:
            return self.handle_server_error(e)

    def delete(self, id):
        """Delete a doctor"""
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return self.handle_not_found("Doctor", id)
            db.session.delete(doctor)
            db.session.commit()
            return {"message": "Doctor deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)