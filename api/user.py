import re
import sqlite3
from flask_restx import Namespace, Resource, fields

from constants import API, DATABASE

# Define namespace
user_namespace = Namespace('users', description='User related operations')

# Define model
user_model = user_namespace.model('User', {
    'email': fields.String(required=True, description='The email address of the user', max_length=128),
    'password': fields.String(required=True, description='The password of the user', max_length=255),
})

def regexp(pattern, data):
    return re.search(pattern, data)

# Define resource
@user_namespace.route('/')
class User(Resource):
    @user_namespace.expect(user_model)
    def post(self):
        user = API.payload
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (email, password)
            VALUES (?, ?)
        """, (user['email'], user['password'],))
            
        email_pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if regexp(email_pattern, user['email']):
            connection.commit()
            connection.close()
            return {'message': 'User created!'}, 201
        else:
            return {'message': 'Invalid email address pattern!'}, 400

    def get(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        connection.close()
        return {'users': users}, 200