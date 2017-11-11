from flask import Flask
from flask_socketio import SocketIO
from .settings import config

app = Flask(__name__)
app.config.from_object(config)

socketio = SocketIO(app)

from . import socket_endpoints
