# -*- coding: utf-8 -*-

"""Django settings for project."""

import datetime
import os

# sqlserver connection string
from djimix.settings.local import MSSQL_EARL
from djimix.settings.local import INFORMIX_ODBC, INFORMIX_ODBC_TRAIN
from djimix.settings.local import (
    INFORMIXSERVER,
    DBSERVERNAME,
    INFORMIXDIR,
    ODBCINI,
    ONCONFIG,
    INFORMIXSQLHOSTS,
    LD_LIBRARY_PATH,
    LD_RUN_PATH,
)

TODAY = datetime.date.today()
# Debug
DEBUG = False
TEMPLATE_DEBUG = DEBUG
INFORMIX_DEBUG = None
ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS
SECRET_KEY = None
ALLOWED_HOSTS = (
    'localhost', '127.0.0.1',
)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = ''
API_URL = '{0}/{1}'.format(SERVER_URL, 'api')
LIVEWHALE_API_URL = 'https://{0}'.format(SERVER_URL)
ROOT_URL = '/library/archives/djpsilobus/'
ROOT_URLCONF = 'djpsilobus.urls'
WSGI_APPLICATION = 'djpsilobus.wsgi.application'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(__file__)
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = '{0}/assets/'.format(BASE_DIR)
MEDIA_URL = '/media/djpsilobus/'
STATIC_ROOT = '{0}/static/'.format(ROOT_DIR)
STATIC_URL = 'https://{0}/static/djpsilobus/'.format(SERVER_URL)
UPLOADS_DIR = '{0}files/'.format(MEDIA_ROOT)
UPLOADS_URL = '{0}files/'.format(MEDIA_URL)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_djsani',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
    },
}
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'djpsilobus',
    'djpsilobus.core',
    # needed for template tags
    'djtools',
)
MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# template stuff
TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
            '/data2/django_templates/djcher/',
            '/data2/django_templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
)
# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60*60*24,
        'KEY_PREFIX': 'DJPSILO_',
    },
}
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = None
LDAP_OBJECT_CLASS = ''
LDAP_GROUPS = None
LDAP_RETURN = ()
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{0}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_NAME = 'django_djpsilobus_cookie'
SESSION_COOKIE_AGE = 86400
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = None
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# dSpace constants
DSPACE_EMAIL = ''
DSPACE_PASSWORD = None
DSPACE_TOKEN = None
DSPACE_JSESSIONID = ''
DSPACE_COOKIE_CACHE_KEY = 'dspace_cookie_cache_key'
DSPACE_URL = ''
DSPACE_REST_URL = '{0}/rest'.format(DSPACE_URL)
# alternative title meta tag for searching for files
DSPACE_TITLE_ALT = 'dc.title.alternative'
# Registrar Administrators
REGISTRAR_ADMIN = ()
# Administrative Assistants
ADMIN_ASSISTANTS = ()
# developers and staff
DEV_ADMIN = ()
ADMINISTRATORS = REGISTRAR_ADMIN + ADMIN_ASSISTANTS + DEV_ADMIN
# year and session for now:
YEAR = TODAY.year
BEGIN_YEAR = 2016
FALL_TERMS = ('RA', 'GA', 'AA', 'AB')
SPRING_TERMS = ('RC', 'AG', 'AK', 'AM', 'GB', 'GC', 'RB')
FACULTY_FULLNAME_LIST_INDEX = 11
# logging
LOG_FILEPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/')
LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
DEBUG_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
INFO_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'info.log')
ERROR_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'error.log')
CUSTOM_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'custom.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'djpsilobus': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
            'class': 'logging.FileHandler',
            'propagate': True,
            'filename': DEBUG_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'djpsilobus.core': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'djauth': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
