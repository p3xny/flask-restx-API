import sqlite3
from flask_restx import Namespace, Resource, fields

from constants import API, DATABASE

# Define namespace
device_namespace = Namespace('devices', description='Device related operations')

# Define model
device_model = device_namespace.model('Device', {
    'serial': fields.String(required=True, description='The serial number of the device', max_length=24),
    'name': fields.String(required=True, description='The name of the device', max_length=128)
})

# Define resource
@device_namespace.route('/')
class Device(Resource):
    @device_namespace.expect(device_model)
    def post(self):
        try:
            device = API.payload
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            
            cursor.execute("INSERT INTO devices (serial, name) VALUES (?, ?)",
                (device['serial'], device['name']))
            
            connection.commit()
            connection.close()
            return {'message': 'Successfully created a new device'}, 200
        except:
            return {'message': 'Invalid request'}, 400

# Returns a list of devices assigned to user
@device_namespace.route('/<int:user_id>')
class GET(Resource):
    def get(self, user_id): 
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        
        if user_id:
            cursor.execute('''
            SELECT users.id, users.email, devices.id,
            devices.name, devices.serial FROM devices
            JOIN accesses ON devices.id = accesses.device_id
            JOIN users ON accesses.user_id = users.id
            WHERE accesses.user_id = ?
            ''', (user_id,))
            devices = cursor.fetchall()

        connection.close()
        return {'devices': devices}