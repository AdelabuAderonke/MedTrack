from flask_restx import Namespace, fields
from app.database import db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from .base_resource import BaseResource

ns = Namespace("appointments", description="Appointment operations")

appointment_model = ns.model("Appointment", {
    "patient_id": fields.Integer(required=True, example=1),
    "doctor_id":  fields.Integer(required=True, example=1),
    "date":       fields.String(required=True, example="2025-03-01"),
    "time":       fields.String(required=True, example="10:00:00"),
    "reason":      fields.String(example="First visit"),
})

@ns.route("/")
class AppointmentList(BaseResource):

    def get(self):
        """Get all appointments"""
        try:
            appointments = Appointment.query.all()
            return [a.to_dict() for a in appointments], 200
        except Exception as e:
            return self.handle_server_error(e)

    @ns.expect(appointment_model, validate=True)
    def post(self):
        """Book an appointment"""
        try:
            data = ns.payload

            # Check patient and doctor exist
            if not Patient.query.get(data["patient_id"]):
                return self.handle_not_found("Patient", data["patient_id"])
            if not Doctor.query.get(data["doctor_id"]):
                return self.handle_not_found("Doctor", data["doctor_id"])

            # Check for slot conflict
            conflict = Appointment.query.filter_by(
                doctor_id=data["doctor_id"],
                date=data["date"],
                time=data["time"]
            ).first()
            if conflict:
                return self.handle_conflict("Doctor already has an appointment at this date and time")

            appointment = Appointment(**data)
            db.session.add(appointment)
            db.session.commit()
            return appointment.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)

@ns.route("/<int:id>")
class AppointmentDetail(BaseResource):

    def get(self, id):
        """Get an appointment by ID"""
        try:
            appointment = Appointment.query.get(id)
            if not appointment:
                return self.handle_not_found("Appointment", id)
            return appointment.to_dict(), 200
        except Exception as e:
            return self.handle_server_error(e)

    def put(self, id):
        """Reschedule or update an appointment"""
        try:
            appointment = Appointment.query.get(id)
            if not appointment:
                return self.handle_not_found("Appointment", id)
            data = ns.payload
            for key, value in data.items():
                setattr(appointment, key, value)
            db.session.commit()
            return appointment.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)

    def delete(self, id):
        """Cancel an appointment"""
        try:
            appointment = Appointment.query.get(id)
            if not appointment:
                return self.handle_not_found("Appointment", id)
            appointment.status = "cancelled"
            db.session.commit()
            return {"message": "Appointment cancelled successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return self.handle_server_error(e)