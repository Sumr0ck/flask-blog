import imp
from app import app
from flask import render_template

from models import Post


@app.route('/')
def index():
    return render_template('index.html')
