
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_managing.settings')

app = Celery('project_managing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
