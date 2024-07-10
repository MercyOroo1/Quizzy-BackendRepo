from flask import  Flask, render_template, url_for, request, redirect
from flask_migrate import Migrate

from datetime import timedelta

from models import db

# from survey import survey_bp
# from response import response_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///survey.db'
app.config['SECRET_KEY'] ='ab1479e159f8b60fc6ade3e987a306'

# app.register_blueprint(survey_bp)

db.init_app(app)

migrate = Migrate(app=app, db=db)












