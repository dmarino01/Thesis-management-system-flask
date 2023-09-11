class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

class DevelpmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB= 'flask_login'

config = {
    'development': DevelpmentConfig
}
