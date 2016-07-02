"""
WSGI config for djproj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys

# python
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.8/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
# django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djskeletor.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/var/cache/python/.python-eggs")
os.environ.setdefault("TZ", "America/Chicago")
# informix
os.environ['INFORMIXSERVER'] = ''
os.environ['DBSERVERNAME'] = ''
os.environ['INFORMIXDIR'] = ''
os.environ['ODBCINI'] = ''
os.environ['ONCONFIG'] = ''
os.environ['INFORMIXSQLHOSTS'] = ''
os.environ['LD_LIBRARY_PATH'] = '$INFORMIXDIR/lib:$INFORMIXDIR/lib/esql:$INFORMIXDIR/lib/tools:/usr/lib/apache2/modules:$INFORMIXDIR/lib/cli'
os.environ['LD_RUN_PATH'] = os.environ['LD_LIBRARY_PATH']
# wsgi
from django.core.wsgi import get_wsgi_application

# NOTE: remove the try/except in production
try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
    exit(-1)

