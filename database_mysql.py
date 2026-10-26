import mysql.connector
from mysql.connector import Error

def get_connection(use_database=True):
    try:
        config = {
            "host": "localhost",
            "user": "root",
            "password": "",  # Default XAMPP MySQL password is empty
            "port": 3306
        }
        if use_database:
            config["database"] = "triintel_db"
        return mysql.connector.connect(**config)
    except Error as e:
        print(f"⚠️ MySQL Connection Error: {e}")
        return None

def initialize_database():
    # 1. Connect without selecting database to ensure it exists
    conn_server = get_connection(use_database=False)
    if not conn_server:
        print("⚠️ Could not connect to XAMPP MySQL. Ensure MySQL is started in XAMPP Control Panel.")
        return

    cursor = conn_server.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS triintel_db;")
    conn_server.commit()
    cursor.close()
    conn_server.close()

    # 2. Connect to triintel_db and create tables
    conn = get_connection(use_database=True)
    if not conn:
        return

    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Role Fit Assessments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_email VARCHAR(255) NOT NULL,
        target_role VARCHAR(100) NOT NULL,
        readiness_score INT NOT NULL,
        submitted_skills TEXT,
        missing_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # DevSecOps Code Audits Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_audits (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_email VARCHAR(255),
        repo_url VARCHAR(255),
        functions_count INT,
        async_count INT,
        classes_count INT,
        maturity_score INT,
        tier VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Connected to XAMPP MySQL & initialized tables in phpMyAdmin.")