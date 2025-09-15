import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('src')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'complete_old_orders_task': {
        'task': 'src.orders.tasks.complete_old_orders',
        'schedule': 10800,
        # 'schedule': 30, # For testing
    },
}
