from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classAssessment.settings')

app = Celery('classAssessment')

# Use settings from Django with CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

    