from flask import Flask, redirect, request, url_for
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Admin
from models import *


class AdminMixin:
    
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class TagModelView(AdminMixin, ModelView):
    form_columns = ['name', 'posts']

    def on_model_change(self, form, model, is_created):
        model.slug = slugify(model.name)
        return super().on_model_change(form, model, is_created)


class PostModelView(AdminMixin, ModelView):
    form_columns = ['title', 'body', 'tags']

    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super().on_model_change(form, model, is_created)


class HomeAdminIndexView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, name='FlaskApp', url='/', index_view=HomeAdminIndexView(name='Home'))
admin.add_views(PostModelView(Post, db.session), TagModelView(Tag, db.session), ModelView(User, db.session))


# Flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
