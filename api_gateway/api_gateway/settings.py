from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-api-gateway-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

# For production EKS, update this to your specific domain/IP
# ALLOWED_HOSTS = ['your-domain.com', 'your-load-balancer-url.amazonaws.com']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'gateway',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'api_gateway.urls'
WSGI_APPLICATION = 'api_gateway.wsgi.application'

DATABASES = {}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os

SERVICES = {
    'user': os.getenv('USER_SERVICE_URL', 'http://localhost:8001'),
    'product': os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:8002'),
    'order': os.getenv('ORDER_SERVICE_URL', 'http://localhost:8003'),
}

# For EKS deployment, set these environment variables:
# USER_SERVICE_URL=http://user-service:8001
# PRODUCT_SERVICE_URL=http://product-service:8002
# ORDER_SERVICE_URL=http://order-service:8003
