import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="hosting_center",
        user="student",
        password="T!gfwo&*24@!gjw!5%"
    )
    print("Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    
    cursor.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
