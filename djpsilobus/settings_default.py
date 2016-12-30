"""
Django settings for project.
"""
#from djzbar.settings import INFORMIX_EARL_TEST as INFORMIX_EARL
from djzbar.settings import INFORMIX_EARL_PROD as INFORMIX_EARL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os.path

# Debug
DEBUG = True
#DEBUG = False
TEMPLATE_DEBUG = DEBUG
INFORMIX_DEBUG = "debug"
ADMINS = (
    ('admin', 'admin@example.com'),
)
MANAGERS = ADMINS
SECRET_KEY = ""
ALLOWED_HOSTS =  ['localhost','127.0.0.1']
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = "www.example.com"
API_URL = "{}/{}".format(SERVER_URL, "api")
LIVEWHALE_API_URL = "https://{}".format(SERVER_URL)
ROOT_URL = "/djpsilobus/"
ROOT_URLCONF = 'djpsilobus.urls'
WSGI_APPLICATION = 'djpsilobus.wsgi.application'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(__file__)
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = '{}/assets/'.format(ROOT_DIR)
#MEDIA_ROOT = ''
#STATIC_ROOT = '{}/static/'.format(ROOT_DIR)
STATIC_ROOT = ''
STATIC_URL = "/static/djpsilobus/"
MEDIA_URL = '{}assets/'.format(STATIC_URL)
UPLOADS_DIR = "{}files/".format(MEDIA_ROOT)
UPLOADS_URL = "{}files/".format(MEDIA_URL)
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
        #'ENGINE': 'django.db.backends.dummy',
        'USER': '',
        'PASSWORD': ''
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'djpsilobus',
    'djpsilobus.core',
    # needed for template tags
    'djtools',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # the following should be uncommented unless you are
    # embedding your apps in iframes
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
            "/data2/django_templates/djkorra/",
            "/data2/django_templates/djcher/",
            "/data2/django_templates/",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "djtools.context_processors.sitevars",
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.core.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            #'loaders': [
            #    # insert your TEMPLATE_LOADERS here
            #]
        },
    },
]
# caching
CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        #'TIMEOUT': None, # never expire
        'TIMEOUT': 60*60*24,
        'KEY_PREFIX': "DJPSILO_",
        'OPTIONS': {
            'MAX_ENTRIES': 500000,
            'CULL_FREQUENCY':20 # cull 5% (1/20) of objects when max_entries
        }
    }
}

# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = ''
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR=''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN=''
SESSION_COOKIE_NAME ='django_djpsilobus_cookie'
SESSION_COOKIE_AGE = 86400
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL=''
# dSpace constants
DSPACE_EMAIL = ""
DSPACE_PASSWORD = ""
DSPACE_TOKEN = ""
DSPACE_URL = "https://dspace.example.com"
DSPACE_REST_URL = "{}/rest".format(DSPACE_URL)
# alternative title meta tag for searching for files
DSPACE_TITLE_ALT = "dc.title.alternative"
# Registrar Administrators
REGISTRAR_ADMIN = []
# Administrative Assistants
ADMIN_ASSISTANTS = []
# developers
DEV_ADMIN = []
ADMINISTRATORS = REGISTRAR_ADMIN + ADMIN_ASSISTANTS + DEV_ADMIN
# year and session for now:
'''
AK  Spring I    UNDG
AM  Spring II   UNDG
AG  Winter
GB  Winter Graduate     GRAD
GC  Spring Graduate     GRAD
RB  J-Term  UNDG
RC  Spring  UNDG
'''
FALL_TERMS = ("RA","GA","AA","AB")
SPRING_TERMS = ("AG","AK","AM","GB","GC","RB","RC")
YEAR=""
#SESS=FALL_TERMS
SESS=SPRING_TERMS
# logging
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'djpsilobus.core': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
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
    }
}
