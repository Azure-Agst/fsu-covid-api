#!/usr/bin/env python3

from flask import Flask

# initialize application
app = Flask(__name__)

# import blueprints
from .blueprints import api, webapp

# register blueprints
app.register_blueprint(
    webapp
)
app.register_blueprint(
    api, url_prefix='/api'
)
