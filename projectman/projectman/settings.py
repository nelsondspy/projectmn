"""
Django settings for projectman project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_DIRS

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n(sgq2=!s=dgw)gmlq@(=nr23jwj*7ryl8rmp!q5*srwi(arw8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'projectman.apps.admin',
    'projectman.apps.desarrollo'
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'projectman.urls'

WSGI_APPLICATION = 'projectman.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.pm.sqlite3'),
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'projectman',
        'USER': 'postgres',
        'PASSWORD':'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
"""

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = ('/static/')


_ROOT_PATH = os.path.dirname(__file__)

TEMPLATE_DIRS=os.path.join(_ROOT_PATH, 'templates')
                     
STATICFILES_DIRS = (  os.path.join(BASE_DIR, 'static'),
('base','/home/nelsonds/projectmn/projectman/projectman/static'))

LOGIN_URL = '/admin/login'


# Sobreescritura del mensaje general de campo requerido 
from django.forms import Field
from django.utils.translation import ugettext_lazy
Field.default_error_messages = {
    'required': ugettext_lazy("Este campo es obligatorio"),
}

SITE_ID = 1 