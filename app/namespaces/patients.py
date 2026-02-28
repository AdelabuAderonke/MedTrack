from flask_restx import Namespace, Resource, fields
from app.models.patient import PatientModel 

ns = Namespace('patients', description='Patient operations')

patient_model = ns.model('Patient', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'gender': fields.String(required=True),
    'email': fields.String(required=True),
    'phone_number': fields.String(required=True)
})

@ns.route('/')
class PatientList(Resource):
    def get(self):
        """List all patients"""
        try:
            # Create instance

            patient_instance = PatientModel()
            # Call methods with self
            patients = patient_instance.get_all()
            total = patient_instance.count()
            return {
                'patients': patients,
                'total': total
            }, 200
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500
    
    @ns.expect(patient_model)
    def post(self):
        """Create a new patient"""
        try:
            
            data = ns.payload
            
            # Check if email already exists
            patient_instance = PatientModel()
            existing = patient_instance.get_by_email(data['email'])
            if existing:
                return {
                    'message': 'Email already registered'
                }, 409
            
            # Create patient
            patient_id = patient_instance.create(data)
            
            # Fetch created patient
            patient = patient_instance.get_by_id(patient_id)
            
            return {
                'message': 'Patient created successfully',
                'patient': patient
            }, 201
        except ValueError as ve:
            return {
                'message': str(ve)
            }, 409
        except Exception as e:
            return {
                'message': 'Server error occurred',
                'error': str(e)
            }, 500

@ns.route('/<int:id>')
class PatientDetail(Resource):
    def get(self, id):
        """Get a patient by ID"""
        try:
            patient_instance = PatientModel()
            patient = patient_instance.get_by_id(id)
            
            if not patient:
                return {'message': f'Patient with ID {id} not found'}, 404
            
            return patient, 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500
    
    @ns.expect(patient_model)
    def put(self, id):
        """Update a patient"""
        try:
            patient_instance = PatientModel()
            if not patient_instance.get_by_id(id):
                ns.abort(404, "Patient not found")
            patient_instance.update(id, ns.payload)
            return {'message': 'Patient updated'}
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500
    
    def delete(self, id):
        """Delete a patient"""
        try:
            patient_instance = PatientModel()
            if not patient_instance.get_by_id(id):
                ns.abort(404, "Patient not found")
            patient_instance.delete_by_id(id)
            return '', 204
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500  
@ns.route('/search')
class PatientSearch(Resource):
    @ns.doc(params={'name': 'Name to search for'})
    def get(self):
        """Search patients by name"""
        try:
            from flask import request
            name = request.args.get('name', '')
            
            if not name:
                return {'message': 'Name parameter is required'}, 400
            
            patient_instance = PatientModel()
            patients = patient_instance.search_by_name(name)
            
            return {
                'patients': patients,
                'total': len(patients)
            }, 200
            
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500