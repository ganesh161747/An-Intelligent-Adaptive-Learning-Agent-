import mysql.connector
from datetime import datetime, timedelta

def seed():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="triintel_db",
        port=3306
    )
    cursor = conn.cursor()

    # 1. Sample Users
    users = [
        ("c.nikhil@mru.edu.in", "student@123"),
        ("priyanka.c@mru.edu.in", "faculty@secure"),
        ("candidate.demo@triintel.com", "pass2026")
    ]
    cursor.executemany("INSERT IGNORE INTO users (email, password) VALUES (%s, %s)", users)

    # 2. Sample Historical Assessments
    assessments = [
        (
            "c.nikhil@mru.edu.in",
            "AI Engineer",
            85,
            "Python, SQL, Machine Learning, Docker",
            "AWS, PyTorch, Deep Learning",
            datetime.now() - timedelta(days=2)
        ),
        (
            "candidate.demo@triintel.com",
            "Data Analyst",
            72,
            "SQL, Excel, Python",
            "Power BI, Statistics, Tableau",
            datetime.now() - timedelta(days=1)
        ),
        (
            "candidate.demo@triintel.com",
            "Cybersecurity Engineer",
            60,
            "Linux, Network Security",
            "Penetration Testing, SIEM Tools, Cryptography",
            datetime.now()
        )
    ]
    cursor.executemany("""
        INSERT INTO assessments 
        (user_email, target_role, readiness_score, submitted_skills, missing_skills, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, assessments)

    # 3. Sample Code Audits (AST Traversal Results)
    audits = [
        (
            "c.nikhil@mru.edu.in",
            "https://github.com/tiangolo/fastapi",
            342,
            84,
            52,
            98,
            "Enterprise Modular Architecture",
            datetime.now() - timedelta(hours=5)
        ),
        (
            "candidate.demo@triintel.com",
            "https://github.com/sample/flask-api",
            45,
            0,
            8,
            42,
            "Foundational Scripting",
            datetime.now() - timedelta(hours=1)
        )
    ]
    cursor.executemany("""
        INSERT INTO code_audits 
        (user_email, repo_url, functions_count, async_count, classes_count, maturity_score, tier, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, audits)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Seed data successfully inserted into triintel_db!")

if __name__ == "__main__":
    seed()