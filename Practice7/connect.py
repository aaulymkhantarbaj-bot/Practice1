# connect.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="phone_user",
        password="ayau2705",
        host="localhost",
        port="5432"
    )