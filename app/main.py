from flask import Flask
from flask_socketio import SocketIO
from .settings import config

app = Flask(__name__)
app.config.from_object(config)

app.config.from_envvar('SECRET_KEY')
socketio = SocketIO(app)

from . import socketio_views
