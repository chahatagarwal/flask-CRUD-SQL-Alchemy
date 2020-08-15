from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import BaseConfig
from flask_migrate import Migrate
import os

MIGRATION_DIR = os.path.join('user', 'migrations')

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)


from user import routes, models    
