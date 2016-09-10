"""
Our config for our webapp.  This is made possible thanks to the from_object() call in Flask.  All uppercase values will be loaded and accessible through the config object in Flask.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__)) # Our init will import this so we can quickly reference the basedir of our app.

WTF_CSRF_ENABLED = True
SECRET_KEY = 'X1L0coaiMfadKVjSPXvufDbBsi'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')