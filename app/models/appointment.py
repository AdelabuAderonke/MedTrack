from app.models.base_model import BaseModel
import mysql.connector

class AppointmentModel(BaseModel):
    """Appointment model - inherits from BaseModel"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "Appointments"
    
    def create(self, appointment_data):
        """Create a new appointment"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            for field in ['reason']:
                if field in appointment_data and any(c in appointment_data[field] for c in [";", "--", "'"]):
                    raise ValueError(f"Invalid characters in {field}")
            self.cursor.execute("""
                INSERT INTO Appointments (patient_id, doctor_id, appointment_date, time, reason, status)
                VALUES (%s, %s, %s, %s, %s, 'scheduled')
            """, (
                appointment_data['patient_id'],
                appointment_data['doctor_id'],
                appointment_data['appointment_date'],
                appointment_data['time'],
                appointment_data.get('reason', '')
            ))
            
            self.conn.commit()
            appointment_id = self.cursor.lastrowid
            self.close_connection()
            return appointment_id
            
        except mysql.connector.Error as err:
            self.conn.rollback()
            self.close_connection()
            raise err
    
    def update(self, appointment_id, appointment_data):
        """Update appointment"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            update_fields = []
            values = []
            
            if 'patient_id' in appointment_data:
                update_fields.append("patient_id = %s")
                values.append(appointment_data['patient_id'])
            
            if 'doctor_id' in appointment_data:
                update_fields.append("doctor_id = %s")
                values.append(appointment_data['doctor_id'])
            
            if 'appointment_date' in appointment_data:
                update_fields.append("appointment_date = %s")
                values.append(appointment_data['appointment_date'])
            
            if 'time' in appointment_data:
                update_fields.append("time = %s")
                values.append(appointment_data['time'])
            
            if 'reason' in appointment_data:
                update_fields.append("reason = %s")
                values.append(appointment_data['reason'])
            
            if 'status' in appointment_data:
                update_fields.append("status = %s")
                values.append(appointment_data['status'])
            
            if not update_fields:
                self.close_connection()
                return False
            
            values.append(appointment_id)
            query = f"UPDATE {self.table_name} SET {', '.join(update_fields)} WHERE id = %s"
            self.cursor.execute(query, values)
            
            self.conn.commit()
            rows_affected = self.cursor.rowcount
            self.close_connection()
            return self._serialize(rows_affected > 0)
            
        except mysql.connector.Error as err:
            self.conn.rollback()
            self.close_connection()
            raise err
    
    def check_conflict(self, doctor_id, date, time, exclude_id=None):
        """Check if doctor has appointment at this time"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        if exclude_id:
            self.cursor.execute("""
                SELECT id FROM Appointments 
                WHERE doctor_id = %s AND appointment_date = %s AND time = %s 
                AND id != %s AND status != 'cancelled'
            """, (doctor_id, date, time, exclude_id))
        else:
            self.cursor.execute("""
                SELECT id FROM Appointments 
                WHERE doctor_id = %s AND appointment_date = %s AND time = %s 
                AND status != 'cancelled'
            """, (doctor_id, date, time))
        
        conflict = self.cursor.fetchone() is not None
        self.close_connection()
        return conflict
    def cancel_appointment(self, appointment_id):
        """Cancel an appointment"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            self.cursor.execute("""
                UPDATE Appointments SET status = 'cancelled' WHERE id = %s
            """, (appointment_id,))
            
            self.conn.commit()
            rows_affected = self.cursor.rowcount
            self.close_connection()
            return rows_affected > 0
            
        except mysql.connector.Error as err:
            self.conn.rollback()
            self.close_connection()
            raise err
    def patient_exists(self, patient_id):
        """Check if patient exists"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            SELECT id FROM Patients WHERE id = %s
        """, (patient_id,))
        
        exists = self.cursor.fetchone() is not None
        self.close_connection()
        return exists
    def doctor_exists(self, doctor_id):
        """Check if doctor exists"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            SELECT id FROM Doctors WHERE id = %s
        """, (doctor_id,))
        
        exists = self.cursor.fetchone() is not None
        self.close_connection()
        return exists   
