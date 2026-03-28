import json
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="office",
    user="postgres",
    password="root"
)

cur = conn.cursor()

# Load JSON file
with open("students_cleaned.json", "r") as file:
    data = json.load(file)

# Insert data
for student in data:
    cur.execute("""
        INSERT INTO students (student_id, name, scholarship_amount, scheme_name, department, year)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (student_id) DO NOTHING
    """, (
        student.get("student_id"),
        student.get("name"),
        student.get("scholarship_amount"),
        student.get("scheme_name"),
        student.get("department"),
        student.get("year")
    ))

# Commit changes
conn.commit()

# Close connection
cur.close()
conn.close()

print("✅ Data inserted successfully!")