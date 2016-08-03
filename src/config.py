class Config:
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # EMAIL SENDER SETTINGS
    MAIL_USERNAME = "kryvonis.artem@gmail.com"
    MAIL_PASSWORD = ""
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # CELERY_SETTINGS
    CELERY_BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'
    CELERY_IMPORTS = 'test_books'
    # LOG FILE SRC

    LOG_FILE = ''
    # URL FOR ELASTICSEARCH
    ES_URL = 'http://elastic:9200'


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig

}
