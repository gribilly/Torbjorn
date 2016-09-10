import os
from flask import Flask
from config import basedir

app = Flask(__name__)
app.config.from_object('config')

# has to be after so that we don't get a conflict with the app.
from torbjorn import views