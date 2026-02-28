from flask_restx import Namespace, fields, Resource

# Import mysql.connector functions
from app.models.appointment import AppointmentModel


ns = Namespace("appointments", description="Appointment operations")

appointment_model = ns.model("Appointment", {
    "patient_id": fields.Integer(required=True, example=1),
    "doctor_id": fields.Integer(required=True, example=1),
    "appointment_date": fields.String(required=True, example="2025-03-01"),
    "time": fields.String(required=True, example="10:00:00"),
    "reason": fields.String(example="First visit"),
})

appointment_update_model = ns.model("AppointmentUpdate", {
    "patient_id": fields.Integer(example=1),
    "doctor_id": fields.Integer(example=1),
    "appointment_date": fields.String(example="2025-03-01"),
    "time": fields.String(example="10:00:00"),
    "reason": fields.String(example="Rescheduled"),
    "status": fields.String(example="scheduled")
})


@ns.route("/")
class AppointmentList(Resource):

    @ns.doc('list_appointments')
    def get(self):
        """Get all appointments"""
        try:
            appointment_instance = AppointmentModel()
            appointments = appointment_instance.get_all()
            return {
                'appointments': appointments,
                'total': len(appointments)
            }, 200
            
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500

    @ns.expect(appointment_model, validate=True)
    @ns.doc('create_appointment')
    def post(self):
        """Book an appointment"""
        try:
            appointment_instance = AppointmentModel()
            data = ns.payload

            # Validate patient exists
            if not appointment_instance.patient_exists(data["patient_id"]):
                return {
                    'message': f'Patient with ID {data["patient_id"]} not found'
                }, 404

            # Validate doctor exists
            if not appointment_instance.doctor_exists(data["doctor_id"]):
                return {
                    'message': f'Doctor with ID {data["doctor_id"]} not found'
                }, 404

            # Check for scheduling conflict
            if appointment_instance.check_conflict(data["doctor_id"], data["appointment_date"], data["time"]):
                return {
                    'message': 'Doctor already has an appointment at this date and time'
                }, 409  # 409 Conflict

            # Create appointment
            appointment_id = appointment_instance.create(data)
            
            # Fetch the created appointment
            appointment = appointment_instance.get_by_id(appointment_id)
            
            return {
                'message': 'Appointment created successfully',
                'appointment': appointment
            }, 201
            
        except Exception as e:
            return {
                'message': 'Failed to create appointment',
                'error': str(e)
            }, 500


@ns.route("/<int:id>")
@ns.param('id', 'The appointment identifier')
class AppointmentDetail(Resource):

    @ns.doc('get_appointment')
    def get(self, id):
        """Get an appointment by ID"""
        try:
            appointment_instance = AppointmentModel()
            appointment = appointment_instance.get_by_id(id)
            
            if not appointment:
                return {
                    'message': f'Appointment with ID {id} not found'
                }, 404
            
            return appointment, 200
            
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500

    @ns.expect(appointment_update_model, validate=True)
    @ns.doc('update_appointment')
    def put(self, id):
        """Reschedule or update an appointment"""
        try:
            appointment_instance = AppointmentModel()
            # Check if appointment exists
            appointment = appointment_instance.exists(id)
            if not appointment:
                return {
                    'message': f'Appointment with ID {id} not found'
                }, 404

            data = ns.payload

            # If updating doctor/date/time, check for conflicts
            if 'doctor_id' in data and 'date' in data and 'time' in data:
                doctor_id = data.get('doctor_id', appointment['doctor_id'])
                date = data.get('date', appointment['date'])
                time = data.get('time', appointment['time'])
                
                if appointment_instance.check_conflict(doctor_id, date, time, exclude_id=id):
                    return {
                        'message': 'Doctor already has an appointment at this date and time'
                    }, 409

            # Validate patient if provided
            if 'patient_id' in data and not appointment_instance.patient_exists(data['patient_id']):
                return {
                    'message': f'Patient with ID {data["patient_id"]} not found'
                }, 404

            # Validate doctor if provided
            if 'doctor_id' in data and not appointment_instance.doctor_exists(data['doctor_id']):
                return {
                    'message': f'Doctor with ID {data["doctor_id"]} not found'
                }, 404

            # Update appointment
            success = appointment_instance.update(id, data)
            
            if success:
                updated_appointment = appointment_instance.get_by_id(id)
                return {
                    'message': 'Appointment updated successfully',
                    'appointment': updated_appointment
                }, 200
            else:
                return {
                    'message': 'Failed to update appointment'
                }, 400
                
        except Exception as e:
            return {
                'message': 'Failed to update appointment',
                'error': str(e)
            }, 500

    @ns.doc('cancel_appointment')
    def delete(self, id):
        """Cancel an appointment"""
        try:
            appointment_instance = AppointmentModel()
            # Check if appointment exists
            appointment = appointment_instance.exists(id)
            if not appointment:
                return {
                    'message': f'Appointment with ID {id} not found'
                }, 404

            # Cancel appointment (soft delete)
            success = appointment_instance.cancel_appointment(id)
            
            if success:
                return {
                    'message': 'Appointment cancelled successfully'
                }, 200
            else:
                return {
                    'message': 'Failed to cancel appointment'
                }, 400
                
        except Exception as e:
            return {
                'message': 'Failed to cancel appointment',
                'error': str(e)
            }, 500