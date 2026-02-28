from app.models.base_model import BaseModel
import mysql.connector

class PatientModel(BaseModel):
    """Patient model - inherits from BaseModel"""
    
    def __init__(self):
        super().__init__()  # Call parent __init__
        self.table_name = "Patients"
    
    def create(self, patient_data):
        """Create a new patient"""
        self.open_connection()
        
        # Switch to regular cursor for INSERT
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            for field in ['name', 'email', 'phone_number']:
                if any(c in patient_data[field] for c in [";", "--", "'"]):
                    raise ValueError(f"Invalid characters in {field}")
            self.cursor.execute("""
                INSERT INTO Patients (name, phone_number, email, gender)
                VALUES (%s, %s, %s, %s)
            """, (
                patient_data['name'],
                patient_data['phone_number'],
                patient_data['email'],
                patient_data['gender']
            ))
            
            self.conn.commit()
            patient_id = self.cursor.lastrowid
            self.close_connection()
            return patient_id
            
        except mysql.connector.IntegrityError as err:
            self.conn.rollback()
            self.close_connection()
            
            if 'email' in str(err):
                raise ValueError("Email already exists")
            elif 'phone_number' in str(err):
                raise ValueError("Phone number already exists")
            else:
                raise err
    
    def update(self, patient_id, patient_data):
        """Update patient information"""
        self.open_connection()
        
        # Switch to regular cursor for UPDATE
        self.cursor.close()
        self.cursor = self.conn.cursor()
        
        try:
            update_fields = []
            values = []
            
            if 'name' in patient_data:
                update_fields.append("name = %s")
                values.append(patient_data['name'])
            
            if 'gender' in patient_data:
                update_fields.append("gender = %s")
                values.append(patient_data['gender'])
            
            if 'email' in patient_data:
                update_fields.append("email = %s")
                values.append(patient_data['email'])
            
            if 'phone_number' in patient_data:
                update_fields.append("phone_number = %s")
                values.append(patient_data['phone_number'])
            
            if not update_fields:
                self.close_connection()
                return False
            
            values.append(patient_id)
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

    
    def search_by_name(self, name):
        """Search patients by name"""
        self.open_connection()
        
        search_pattern = f"%{name}%"
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE name LIKE %s",
            (search_pattern,)
        )
        results = self.cursor.fetchall()
        
        self.close_connection()
        
        return self._serialize(results)
    def get_by_email(self, email):
        """Find patient by email"""
        self.open_connection()
        
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE email = %s",
            (email,)
        )
        result = self.cursor.fetchone()
        
        self.close_connection()
        
        return self._serialize(result)