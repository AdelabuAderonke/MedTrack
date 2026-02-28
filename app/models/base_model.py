import mysql.connector
from datetime import datetime, date, timedelta

class BaseModel:
    """Base class for all models"""
    
    table_name = None  # don't create table for base model
    
    def __init__(self):
        """Initialize the model"""
        self.conn = None
        self.cursor = None
    
    def get_connection(self):
        """Get database connection"""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="MedDB"
        )
    
    def open_connection(self):
        """Open database connection"""
        self.conn = self.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)
    
    def close_connection(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    def _serialize(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        
        if isinstance(obj, timedelta):
            return str(obj)  

        if isinstance(obj, dict):
            return {key: self._serialize(value) for key, value in obj.items()}

        if isinstance(obj, list):
            return [self._serialize(item) for item in obj]

        return obj
    
    def get_all(self):
        """Get all records from table"""
        self.open_connection()
        
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        results = self.cursor.fetchall()
        
        self.close_connection()
        
        return self._serialize(results)
    
    def get_by_id(self, record_id):
        """Find record by ID"""
        self.open_connection()
        
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (record_id,))
        result = self.cursor.fetchone()
        
        self.close_connection()
        
        return self._serialize(result)
    
    def delete_by_id(self, record_id):
        """Delete record by ID"""
        self.open_connection()
        
        try:
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (record_id,))
            self.conn.commit()
            rows_affected = self.cursor.rowcount
            self.close_connection()
            return rows_affected > 0
            
        except mysql.connector.IntegrityError:
            self.conn.rollback()
            self.close_connection()
            raise ValueError(f"Cannot delete {self.table_name[:-1]} with existing relationships")
    
    def count(self):
        """Count total records"""
        self.open_connection()
        
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        count = self.cursor.fetchone()
        result = list(count.values())[0] if count else 0
        
        self.close_connection()
        
        return result
    
    def exists(self, record_id):
        """Check if record exists"""
        self.open_connection()
        
        self.cursor.execute(f"SELECT id FROM {self.table_name} WHERE id = %s", (record_id,))
        exists = self.cursor.fetchone() is not None
        
        self.close_connection()
        
        return exists
    