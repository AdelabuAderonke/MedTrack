from flask_restx import Namespace, fields, Resource
from app.models.doctor import DoctorModel

ns = Namespace("doctors", description="Doctor operations")
# API Models
doctor_model = ns.model("Doctor", {
    "name": fields.String(required=True, example="Dr. Sarah Smith"),
    "gender": fields.String(required=True, example="Female"),
    "specialization": fields.String(required=True, example="Cardiology"),
    "email": fields.String(required=True, example="dr.smith@hospital.com"),
    "phone_number": fields.String(required=True, example="555-0123")
})

doctor_update_model = ns.model("DoctorUpdate", {
    "name": fields.String(example="Dr. Sarah Smith"),
    "gender": fields.String(example="Female"),
    "specialization": fields.String(example="Cardiology"),
    "email": fields.String(example="dr.smith@hospital.com"),
    "phone_number": fields.String(example="555-0123")
})


@ns.route("/")
class DoctorList(Resource):

    @ns.doc('list_doctors')
    @ns.param('specialization', 'Filter by specialization', required=False)
    @ns.param('search', 'Search by name or specialization', required=False)
    def get(self):
        """Get all doctors with optional filters"""
        try:
            from flask import request
            doctor_instance = DoctorModel()
            doctors = doctor_instance.get_all()
            total = doctor_instance.count()
            
            specialization = request.args.get('specialization')
            search_term = request.args.get('search')
            
            if search_term:
                doctors = doctor_instance.search_by_name(search_term)
                total = len(doctors)
            elif specialization:
                doctors = doctor_instance.find_by_specialization(specialization)
                total = len(doctors)
            else:
                doctors = doctor_instance.get_all()
                
            
            return {
                'doctors': doctors,
                'total': total
            }, 200
            
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500

    @ns.expect(doctor_model, validate=True)
    @ns.doc('create_doctor')
    def post(self):
        """Register a new doctor"""
        try:
            doctor_instance = DoctorModel()
            data = ns.payload
            
            # Check if email already exists
            if doctor_instance.get_by_email(data['email']):
                return {
                    'message': 'Email already registered'
                }, 409
            
            
            # Create doctor
            doctor_id = doctor_instance.create(data)
            
            # Fetch created doctor
            doctor = doctor_instance.get_by_id(doctor_id)
            
            return {
                'message': 'Doctor registered successfully',
                'doctor': doctor
            }, 201
            
        except ValueError as e:
            return {
                'message': str(e)
            }, 409
            
        except Exception as e:
            return {
                'message': 'Failed to register doctor',
                'error': str(e)
            }, 500


@ns.route("/<int:id>")
@ns.param('id', 'The doctor identifier')
class DoctorDetail(Resource):

    @ns.doc('get_doctor')
    def get(self, id):
        """Get a doctor by ID"""
        try:
            doctor_instance = DoctorModel()
            doctor = doctor_instance.get_by_id(id)
            
            if not doctor:
                return {
                    'message': f'Doctor with ID {id} not found'
                }, 404
            
            return doctor, 200
            
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500

    @ns.expect(doctor_update_model, validate=True)
    @ns.doc('update_doctor')
    def put(self, id):
        """Update doctor information"""
        try:
            # Check if doctor exists
            doctor_instance = DoctorModel()
            doctor = doctor_instance.exists(id)
            if not doctor:
                return {
                    'message': f'Doctor with ID {id} not found'
                }, 404
            
            data = ns.payload
            
            # Check email uniqueness if updating email
            if 'email' in data and data['email'] != doctor['email']:
                existing = doctor_instance.get_by_email(data['email'])
                if existing and existing['id'] != id:
                    return {
                        'message': 'Email already in use'
                    }, 409
            
            # Update doctor
            success = doctor_instance.update(id, data)
            
            if success:
                updated_doctor = doctor_instance.get_by_id(id)
                return {
                    'message': 'Doctor updated successfully',
                    'doctor': updated_doctor
                }, 200
            else:
                return {
                    'message': 'No changes made'
                }, 400
                
        except ValueError as e:
            return {
                'message': str(e)
            }, 409
            
        except Exception as e:
            return {
                'message': 'Failed to update doctor',
                'error': str(e)
            }, 500

    @ns.doc('delete_doctor')
    def delete(self, id):
        """Delete a doctor"""
        try:
            # Check if doctor exists
            doctor_instance = DoctorModel()
            doctor = doctor_instance.get_by_id(id)
            if not doctor:
                return {
                    'message': f'Doctor with ID {id} not found'
                }, 404  
            
            # Delete doctor
            success = doctor_instance.delete_by_id(id)
            
            if success:
                return {
                    'message': 'Doctor deleted successfully'
                }, 200
            else:
                return {
                    'message': 'Failed to delete doctor'
                }, 400
                
        except ValueError as e:
            return {
                'message': str(e)
            }, 409
            
        except Exception as e:
            return {
                'message': 'Failed to delete doctor',
                'error': str(e)
            }, 500


@ns.route("/<int:id>/appointments")
@ns.param('id', 'The doctor identifier')
class DoctorAppointments(Resource):

    @ns.doc('get_doctor_appointments')
    def get(self, id):
        """Get all appointments for a doctor"""
        try:
            # Check if doctor exists
            doctor_instance = DoctorModel()
            doctor = doctor_instance.exists(id)
            if not doctor:
                return {
                    'message': f'Doctor with ID {id} not found'
                }, 404
            doctor = doctor_instance.get_by_id(id)
            appointments = doctor_instance.get_by_appointments(id)
            
            return {
                'doctor': {
                    'id': doctor['id'],
                    'name': doctor['name'],
                    'specialization': doctor['specialization']
                },
                'appointments': appointments,
                'total': len(appointments)
            }, 200
            
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500


@ns.route("/<int:id>/availability")
@ns.param('id', 'The doctor identifier')
@ns.param('date', 'Date in YYYY-MM-DD format', required=True)
class DoctorAvailability(Resource):

    @ns.doc('get_doctor_availability')
    def get(self, id):
        """Check doctor's availability for a specific date"""
        try:
            doctor_instance = DoctorModel()
            from flask import request
            
            date = request.args.get('date')
            if not date:
                return {
                    'message': 'Date parameter is required (format: YYYY-MM-DD)'
                }, 400
            
            # Check if doctor exists
            doctor = doctor_instance.get_by_id(id)
            if not doctor:
                return {
                    'message': f'Doctor with ID {id} not found'
                }, 404
            
            booked_slots = doctor_instance.get_by_availability(id,date)
            
            return {
                'doctor': {
                    'id': doctor['id'],
                    'name': doctor['name'],
                    'specialization': doctor['specialization']
                },
                'date': date,
                'booked_slots': booked_slots,
                'total_bookings': len(booked_slots)
            }, 200
            
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500