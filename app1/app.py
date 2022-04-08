from msilib import Table
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *

admin = Admin(app)
admin.add_views(ModelView(Post, db.session), ModelView(Tag, db.session))
