class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

class DevelpmentConfig(Config):
    DEBUG=True

config = {
    'development': DevelpmentConfig
}
