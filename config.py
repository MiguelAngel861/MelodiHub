# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '63f4945d921d599f27ae4fdf5bada3f1')
    SERVER_NAME = 'lunarblade.net'

    # Flask-Bcrypt
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', 12))
    BCRYPT_HANDLE_LONG_PASSWORDS = os.getenv(
        'BCRYPT_HANDLE_LONG_PASSWORDS', 'true'
    ).lower() in ('true', '1', 't')

    # Flask-WTF
    WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED', 'true').lower() in ('true', '1', 't')
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', SECRET_KEY)
    WTF_CSRF_TIME_LIMIT = int(os.getenv('WTF_CSRF_TIME_LIMIT', 3600))

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'true').lower() in ('true', '1', 't')

    # Flask-Login
    LOGIN_VIEW = os.getenv('LOGIN_VIEW', 'auth.login')
    LOGIN_MESSAGE = os.getenv('LOGIN_MESSAGE', 'Por favor inicia sesión para acceder a esta página.')
    LOGIN_MESSAGE_CATEGORY = os.getenv('LOGIN_MESSAGE_CATEGORY', 'warning')
    SESSION_PROTECTION = os.getenv('SESSION_PROTECTION', 'strong')
    REMEMBER_COOKIE_DURATION = timedelta(days = int(os.environ.get('REMEMBER_COOKIE_DURATION_DAYS', 7)))
    REMEMBER_COOKIE_SECURE = os.getenv('REMEMBER_COOKIE_SECURE', 'true').lower() in ('true', '1', 't')
    REMEMBER_COOKIE_HTTPONLY = os.getenv('REMEMBER_COOKIE_HTTPONLY', 'true').lower() in ('true', '1', 't')
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = os.getenv('REMEMBER_COOKIE_REFRESH', 'false').lower() in ('true', '1', 't')

    # Paginación
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))

    # Caché (Redis)
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Celery (tareas asíncronas)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', CACHE_REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', CACHE_REDIS_URL)

    # Logging
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'false').lower() in ('true', '1', 't')


class DevelopmentConfig(Config):
    sql = Credentials()

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{sql.mysql_user}:{sql.mysql_pwsd}@{sql.mysql_host}:{sql.mysql_port}/{sql.mysql_db}'
    TEMPLATES_AUTO_RELOAD = True
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', 4))


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', '')
    LOG_TO_STDOUT = False
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    )
    TEMPLATES_AUTO_RELOAD = False
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', 12))

