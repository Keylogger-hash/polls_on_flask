import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsdkfd32r234fsdf'
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///polls.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'

    ################
    # Flask-Security
    ################

    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "fsdfdfsdfdfsdafds"
