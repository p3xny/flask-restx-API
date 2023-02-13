from flask import Flask, Blueprint
from flask_restx import Api

APP = Flask(__name__)
BLUEPRINT = Blueprint('api', __name__)
API = Api(BLUEPRINT)
DATABASE = 'devices-kw01.db'