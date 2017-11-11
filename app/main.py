from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from .settings import config

app = Flask(__name__)
app.config.from_object(config)
CORS(app)

socketio = SocketIO(app)

from . import socket_endpoints
