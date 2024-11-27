"""
WSGI config for youth project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from flask_app.wsgi import flask_app  # Flask 앱 임포트
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youth.settings')

application = get_wsgi_application()
application.wsgi_app = flask_app.wsgi_app  # Flask 애플리케이션 연결