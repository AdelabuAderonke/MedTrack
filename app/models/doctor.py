from app.models.base_model import BaseModel
import mysql.connector

class DoctorModel(BaseModel):
    """Doctor model - inherits from BaseModel"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "Doctors"
    
    def create(self, doctor_data):
        """Create a new doctor"""
        self.open_connection()
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            self.cursor.execute("""
                INSERT INTO Doctors (name, gender, specialization, email, phone_number)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                doctor_data['name'],
                doctor_data['gender'],
                doctor_data['specialization'],
                doctor_data['email'],
                doctor_data['phone_number']
            ))
            
            self.conn.commit()
            doctor_id = self.cursor.lastrowid
            self.close_connection()
            return doctor_id
            
        except mysql.connector.IntegrityError as err:
            self.conn.rollback()
            self.close_connection()
            
            if 'email' in str(err):
                raise ValueError("Email already exists")
            elif 'phone_number' in str(err):
                raise ValueError("Phone number already exists") 
                raise err
    
    def update(self, doctor_id, doctor_data):
        """Update doctor information"""
        self.open_connection()
        
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            update_fields = []
            values = []
            
            if 'name' in doctor_data:
                update_fields.append("name = %s")
                values.append(doctor_data['name'])
        
            if 'gender' in doctor_data:
                update_fields.append("gender = %s")
                values.append(doctor_data['gender'])
            
            if 'specialization' in doctor_data:
                update_fields.append("specialization = %s")
                values.append(doctor_data['specialization'])
            
            if 'email' in doctor_data:
                update_fields.append("email = %s")
                values.append(doctor_data['email'])
            
            if 'phone_number' in doctor_data:
                update_fields.append("phone_number = %s")
                values.append(doctor_data['phone_number'])
            
            if not update_fields:
                self.close_connection()
                return False
            
            values.append(doctor_id)
            query = f"UPDATE {self.table_name} SET {', '.join(update_fields)} WHERE id = %s"
            self.cursor.execute(query, values)
            
            self.conn.commit()
            rows_affected = self.cursor.rowcount
            self.close_connection()
            return rows_affected > 0
            
        except mysql.connector.IntegrityError as err:
            self.conn.rollback()
            self.close_connection()
            
            if 'email' in str(err):
                raise ValueError("Email already exists")
            elif 'phone_number' in str(err):
                raise ValueError("Phone number already exists")
            else:
                raise err
    
    def find_by_specialization(self, specialization):
        """Find doctors by specialization"""
        self.open_connection()
        
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE specialization = %s",
            (specialization,)
        )
        results = self.cursor.fetchall()
        
        self.close_connection()
        return self._serialize(results)
    
    def get_by_appointments(self, appointment_id):
        """Find doctor by appointment ID"""
        self.open_connection()
        
        self.cursor.execute(
            f"""
            SELECT d.* FROM {self.table_name} d
            JOIN Appointments a ON d.id = a.doctor_id
            WHERE a.id = %s
            """,
            (appointment_id,)
        )
        result = self.cursor.fetchone()
        
        self.close_connection()
        return self._serialize(result)

    def get_by_availability(self, id, date):
        """Find doctors by availability"""
        self.open_connection()
        
        self.cursor.execute(
            f"""
                SELECT * FROM Appointments
                WHERE doctor_id = %s AND appointment_date = %s AND status = 'scheduled'
            """,
            (id,date)
        )
        results = self.cursor.fetchall()
        
        self.close_connection()
        return self._serialize(results)
    
    def get_by_email(self, email):
        """Find doctor by email"""
        self.open_connection()
        
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE email = %s",
            (email,)
        )
        result = self.cursor.fetchone()
        
        self.close_connection()
        return self._serialize(result)