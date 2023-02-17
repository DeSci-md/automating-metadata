from flask import Blueprint, request
from dotenv import load_dotenv
import psycopg2
import os

database_connection = Blueprint('database_connection', __name__)

load_dotenv()
url = os.getenv("DATABASE_URL")
print("DATABASE",url)
connection = psycopg2.connect(dsn=url, user='postgres')

# PostgreSQL queries
CREATE_USERS_TABLE = (
    'CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, address TEXT);'
)
CREATE_PLANETS_TABLE = (
    """CREATE TABLE IF NOT EXISTS planets (user_id INTEGER, temperature REAL, date TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);"""
)
INSERT_USER_RETURN_ID = 'INSERT INTO users (address) VALUES (%s) RETURNING id;'
INSERT_PLANET = (
    'INSERT INTO planets (user_id, temperature, date) VALUES (%s, %s, %s);'
)

# User Management
@database_connection.post('/api/user')
def addUser():
    data = request.get_json()
    address = data['address']

    # Connect to the database
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID, (address,))
            user_id = cursor.fetchone()[0]

    return {'id': user_id, 'message': f"User {address} created"}, 201