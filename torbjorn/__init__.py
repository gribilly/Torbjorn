import os
from flask import Flask
from config import basedir

app = Flask(__name__)
app.config.from_object('config')

# Technically a circular import, but according to Flask docs this is ok and desired: http://flask.pocoo.org/docs/0.11/patterns/packages/
from torbjorn import views