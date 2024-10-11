import os

import django.conf
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_server.settings")
app = Celery("blog_server")
app.config_from_object(django.conf.settings, namespace="CELERY")
app.autodiscover_tasks()