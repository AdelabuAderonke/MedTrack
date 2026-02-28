import unittest
from app.models.appointment import AppointmentModel
from app.models.doctor import DoctorModel
from app.models.patient import PatientModel
from app.models.base_model import BaseModel

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.patient_model = PatientModel()
        self.doctor_model = DoctorModel()
        self.appointment_model = AppointmentModel()

    def test_patient_creation_update_delete(self):
        #create patient
        patient_data = {
            'name': 'John Doe',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'gender': 'Male'
        }
        patient_id = self.patient_model.create(patient_data)
        self.assertIsNotNone(patient_id)
        
        #update patient
        updated_data = {
            'name': 'John Smith',
            'phone_number': '0987654321',
            'email': 'john.smith@example.com',
            'gender': 'Male'}
        self.assertTrue(self.patient_model.update(patient_id, updated_data))
        
        #delete patient
        self.assertTrue(self.patient_model.delete_by_id(patient_id))
    #Test doctor creation, update and delete
    def test_doctor_creation_update_delete(self):
        doctor_data = {
            'name': 'Dr. Jane Doe',
            'specialization': 'Cardiology',
            'phone_number': '555-1234',
            'email': 'jane.doe@example.com',
            'gender': 'Female'  
        }
        doctor_id = self.doctor_model.create(doctor_data)
        self.assertIsNotNone(doctor_id)

        # Update doctor
        updated_doctor_data = {
            'name': 'Dr. Jane Smith',
            'specialization': 'Neurology',
            'phone_number': '555-5678',
            'email': 'jane.smith@example.com'
        }
        self.assertTrue(self.doctor_model.update(doctor_id, updated_doctor_data))

        # Delete doctor
        self.assertTrue(self.doctor_model.delete_by_id(doctor_id))

    #Test appointment creation, update and delete
    def test_appointment_creation_update_delete(self):
        # First, create a patient and a doctor to associate with the appointment
        patient_data = {
            'name': 'Alice Johnson',
            'phone_number': '555-9876',
            'email': 'alice.johnson@example.com',
            'gender': 'Female'
        }
        patient_id = self.patient_model.create(patient_data)
        self.assertIsNotNone(patient_id)

        doctor_data = {
            'name': 'Dr. Bob Smith',
            'specialization': 'Pediatrics',
            'phone_number': '555-4321',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }
        doctor_id = self.doctor_model.create(doctor_data)
        self.assertIsNotNone(doctor_id)

        # Create appointment
        appointment_data = {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_date': '2023-01-01',
            'time': '10:00',
            'status': 'Scheduled'
        }
        appointment_id = self.appointment_model.create(appointment_data)
        self.assertIsNotNone(appointment_id)

        # Update appointment
        updated_appointment_data = {
            'appointment_date': '2023-01-02',
            'time': '11:00',
            'status': 'Confirmed'
        }
        self.assertTrue(self.appointment_model.update(appointment_id, updated_appointment_data))

        # Delete appointment
        self.assertTrue(self.appointment_model.delete_by_id(appointment_id))

if __name__ == '__main__':
    unittest.main()