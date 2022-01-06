#!/usr/bin/env python3

from flask import Flask, g

# initialize application
app = Flask(__name__)

# import blueprints
from .blueprints import api

# register blueprints
app.register_blueprint(api)
