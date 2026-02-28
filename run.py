from flask import Flask
from flask_restx import Api
from flask.json.provider import DefaultJSONProvider
from datetime import datetime, date

# Import namespaces
from app.namespaces.patients import ns as patients_ns
from app.namespaces.doctors import ns as doctors_ns
from app.namespaces.appointments import ns as appointments_ns


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


app = Flask(__name__)

# ✅ IMPORTANT: set provider CLASS (not instance)
app.json_provider_class = CustomJSONProvider

# Reinitialize json system
app.json = app.json_provider_class(app)

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