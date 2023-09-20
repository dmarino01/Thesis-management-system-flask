from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/thesis_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=True

db = SQLAlchemy()
csrf = CSRFProtect()