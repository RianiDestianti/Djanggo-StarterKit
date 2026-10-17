import os
import sys
from dotenv import load_dotenv
from config.database import database

load_dotenv()

REQUIRED_ENV = ['DB_HOST', 'DB_USER', 'DB_NAME', 'JWT_SECRET']

if os.getenv('DB_CLIENT') == 'sqlite':
    REQUIRED_ENV = ['DB_NAME', 'JWT_SECRET']

missing = [key for key in REQUIRED_ENV if not os.getenv(key)]
if missing:
    print(f"[error] Env wajib belum diisi: {', '.join(missing)}")
    sys.exit(1)

SECRET_KEY          = os.getenv('APP_KEY') or os.getenv('JWT_SECRET')
DEBUG               = os.getenv('APP_DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS       = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'corsheaders',
    'models',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'middleware.exception_middleware.ExceptionMiddleware',
]

ROOT_URLCONF        = 'config.urls'
WSGI_APPLICATION    = 'config.wsgi.application'

DATABASES = {
    'default': database(),
}

DEFAULT_AUTO_FIELD  = 'django.db.models.AutoField'
APPEND_SLASH        = False
USE_TZ              = False
TIME_ZONE           = os.getenv('TIME_ZONE', 'Asia/Jakarta')
LANGUAGE_CODE       = 'en-us'

CORS_ALLOW_ALL_ORIGINS  = os.getenv('CORS_ORIGIN', '*') == '*'
CORS_ALLOWED_ORIGINS    = [] if CORS_ALLOW_ALL_ORIGINS else os.getenv('CORS_ORIGIN', '').split(',')
CORS_ALLOW_METHODS      = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS      = ['content-type', 'authorization']

LOGGING = {
    'version'                   : 1,
    'disable_existing_loggers'  : False,
    'handlers'                  : { 'console': { 'class': 'logging.StreamHandler' } },
    'root'                      : { 'handlers': ['console'], 'level': 'WARNING' },
}
