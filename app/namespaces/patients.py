from flask_restx import Namespace, fields
from app.database import db
from app.models.patient import Patient
from .base_resource import BaseResource

ns = Namespace("patients", description="Patient CRUD operations")

patient_model = ns.model("Patient", {
    "name": fields.String(required=True, example="Jane Doe"),
    "email":     fields.String(required=True, example="jane@email.com"),
    "phone":     fields.String(example="07700900000"),
    "gender":       fields.String(example="Female"),
})

@ns.route("/")
class PatientList(BaseResource):

    def get(self):
        """Get all patients"""
        try:
            patients = Patient.query.all()
            return [p.to_dict() for p in patients], 200
        except Exception as e:
            return self.handle_server_error(e)

    @ns.expect(patient_model, validate=True)
    def post(self):
        """Register a new patient"""
        try:
            data = ns.payload
            existing = Patient.query.filter_by(email=data["email"]).first()
            if existing:
                return self.handle_conflict("A patient with this email already exists")
            patient = Patient(**data)
            db.session.add(patient)
            db.session.commit()
            return patient.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)

@ns.route("/<int:id>")
class PatientDetail(BaseResource):

    def get(self, id):
        """Get a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return self.handle_not_found("Patient", id)
            return patient.to_dict(), 200
        except Exception as e:
            return self.handle_server_error(e)

    @ns.expect(patient_model)
    def put(self, id):
        """Update a patient"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return self.handle_not_found("Patient", id)
            data = ns.payload
            for key, value in data.items():
                setattr(patient, key, value)
            db.session.commit()
            return patient.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)

    def delete(self, id):
        """Delete a patient"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return self.handle_not_found("Patient", id)
            db.session.delete(patient)
            db.session.commit()
            return {"message": "Patient deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)