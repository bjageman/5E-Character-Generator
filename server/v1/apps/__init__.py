from flask import Flask
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import timedelta

from . import config

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'AO0bqSHRFMyMUgzaw0Vx2FkLkkAr3Gpe'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=24)

db = SQLAlchemy(app)
db.init_app(app)
#Web Socket
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

from .users import users
from .characters import characters

#JWT System

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(characters, url_prefix='/api/v1/characters')

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response
