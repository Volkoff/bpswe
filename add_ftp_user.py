import psycopg2

conn = psycopg2.connect(
    dbname="hosting_center",
    user="student",
    password="T!gfwo&*24@!gjw!5%",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
cur.execute("INSERT INTO ftp_accounts (username, password_hash, directory) VALUES ('testftp', 'pass', '/var/www/html/testftp')")
conn.commit()
conn.close()
print("Success")
