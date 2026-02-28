import unittest
from app.models.doctor import DoctorModel
from app.models.appointment import AppointmentModel
from app.models.patient import PatientModel

class TestPatientInjectionProtection(unittest.TestCase):
    def setUp(self):
        self.patient_model = PatientModel()

    def test_sql_injection_prevention(self):
        """Verify that SQL injection attempts don't bypass security"""
        # Attempt injection
        injection_string = "'; DROP TABLE patients; --"
        patient_data = {
            'name': injection_string,
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'gender': 'Male'
        }

        
        with self.assertRaises(ValueError):
            self.patient_model.create(patient_data)
class TestDoctorInjectionProtection(unittest.TestCase):
    def setUp(self):
        self.doctor_model = DoctorModel()

    def test_sql_injection_prevention(self):
        """Verify that SQL injection attempts don't bypass security"""
        # Attempt injection
        injection_string = "'; DROP TABLE doctors; --"
        doctor_data = {
            'name': injection_string,
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'specialty': 'General Practitioner'
        }

        
        with self.assertRaises(ValueError):
            self.doctor_model.create(doctor_data)
class TestAppointmentInjectionProtection(unittest.TestCase):
    def setUp(self):
        self.appointment_model = AppointmentModel()

    def test_sql_injection_prevention(self):
        """Verify that SQL injection attempts don't bypass security"""
        # Attempt injection
        injection_string = "'; DROP TABLE appointments; --"
        appointment_data = {
            'patient_id': 1,
            'doctor_id': 1,
            'appointment_date': '2024-07-01',
            'reason': injection_string,
            'status': 'scheduled',
            'time': '10:00:00'
        }

        
        with self.assertRaises(ValueError):
            self.appointment_model.create(appointment_data) 
if __name__ == '__main__':
    unittest.main()