import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
         
        
    )
def setup_MedDB():
    conn = get_connection()
    cursor = conn.cursor()
    print("Creating 'Medtrack' database...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS MedDB")
    cursor.execute("USE MedDB")
    
    # Create Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        phone_number VARCHAR(255),
        email VARCHAR(255),
        gender VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""")
    #insert dummy data into patients table
    patients = [
        (1, 'John Doe', '1234567890', 'john@example.com', 'Male',"2024-07-01 10:00:00", "2024-07-01 10:00:00"),
        (2, 'Jane Smith', '0987654321', 'jane@example.com', 'Female',"2024-07-01 10:00:00", "2024-07-01 10:00:00"),
        (3, 'Alice Johnson', '5555555555', 'alice@example.com', 'Female',"2024-07-01 10:00:00", "2024-07-01 10:00:00")
    ]
    cursor.executemany("INSERT IGNORE INTO Patients VALUES (%s, %s, %s, %s, %s, %s, %s)", patients)
    # Create Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        gender VARCHAR(255),
        specialization VARCHAR(255),
        email VARCHAR(255),
        phone_number VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )""")
    # Insert dummy data into doctors table
    doctors = [
        (1, 'Dr. John Smith', 'Male', 'Cardiology', 'john@hospital.com', '555-0123',"2024-07-01 10:00:00", "2024-07-01 10:00:00"),
        (2, 'Dr. Jane Doe', 'Female', 'Neurology', 'jane@hospital.com', '555-0456',"2024-07-01 10:00:00", "2024-07-01 10:00:00"),
        (3, 'Dr. Alice Johnson', 'Female', 'Pediatrics', 'alice@hospital.com', '555-0789',"2024-07-01 10:00:00", "2024-07-01 10:00:03")
    ]
    cursor.executemany("INSERT IGNORE INTO Doctors VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", doctors)
    # Create Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Appointments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        doctor_id INT,
        appointment_date DATE,
        reason VARCHAR(255),
        status VARCHAR(255),
        time TIME,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES Patients(id),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
    )""")
    # Insert dummy data into appointments table
    appointments = [
        (1, 1, 1, '2024-07-01', 'Regular Checkup', 'scheduled','10:00:00', '2024-07-01 10:00:00','2024-07-01 10:00:00'),
        (2, 2, 2, '2024-07-02', 'Headache', 'scheduled','11:30:00', '2024-07-01 11:35:35','2024-07-01 11:35:35'),
        (3, 3, 3, '2024-07-03', 'Child Fever', 'scheduled','14:45:00', '2024-07-01 14:55:35','2024-07-01 14:55:35')
    ]
    cursor.executemany("INSERT IGNORE INTO Appointments VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", appointments)
    conn.commit()
    cursor.close()  
    conn.close()

 #to create database I had to include the main block here   
if __name__ == "__main__":
    setup_MedDB()
    print("MedTrack Database Setup successful!")
        