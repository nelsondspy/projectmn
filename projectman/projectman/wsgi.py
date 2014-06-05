"""
WSGI config for projectman project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
path = '/var/www/projectman/'
if path not in sys.path:
    sys.path.append(path)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectman.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
