from flask import Flask
from flask_restx import Api
from app.config import Config
from app.database import db, migrate

# Import models so Flask-Migrate can detect them
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment

# Import namespaces
from app.namespaces.patients import ns as patients_ns
from app.namespaces.doctors import ns as doctors_ns
from app.namespaces.appointments import ns as appointments_ns

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

api = Api(
    app,
    title="MedTrack API",
    version="1.0",
    description="Hospital Appointment Management System",
    doc="/docs"
)

api.add_namespace(patients_ns, path="/patients")
api.add_namespace(doctors_ns, path="/doctors")
api.add_namespace(appointments_ns, path="/appointments")

if __name__ == "__main__":
    app.run(debug=True)