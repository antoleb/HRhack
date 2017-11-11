from flask import Flask
from .settings import config

app = Flask(__name__)
app.config.from_object(config)

from . import views
from . import endpoints
