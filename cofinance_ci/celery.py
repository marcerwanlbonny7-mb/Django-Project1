import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cofinance_ci.settings')

app = Celery('cofinance_ci')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
