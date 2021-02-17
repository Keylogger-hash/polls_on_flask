from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


def create_app():
    app = Flask(__name__,template_folder='flaskr/templates')
    app.config.from_object(Config)
    app.config.from_pyfile('config-extended.py')

    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app,db)
