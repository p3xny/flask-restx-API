import sqlite3
from flask_restx import Namespace, Resource, fields

from constants import API, DATABASE

# Define namespace
access_namespace = Namespace('access', description='Access related operations')

# Define model
access_model = access_namespace.model('Access', {
    'user_id': fields.Integer(required=True, description='ID of the user'),
    'device_id': fields.Integer(required=True, description='ID of the device'),
})

# Define resource
@access_namespace.route('/')
class Access(Resource):
    @access_namespace.expect(access_model)
    def post(self):
        access = API.payload
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO accesses (user_id, device_id) VALUES (?, ?)",
            (access['user_id'], access['device_id']))
        
        connection.commit()
        connection.close()
        return {'message': 'Access granted!'}, 201
    
    def get(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accesses')
        accesses = cursor.fetchall()
        
        connection.close()
        return {'accesses': accesses}

    @access_namespace.expect(access_model)
    def delete(self):
        access = API.payload
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute('DELETE FROM accesses WHERE user_id = ? AND device_id = ?' ,
        (access['user_id'], access['device_id']))
        
        connection.commit()
        connection.close()
        return {'message': 'Access removed!'}, 200

