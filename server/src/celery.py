import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('src')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'cleanup_expired_bags_task': {
        'task': 'src.shopping_bags.tasks.cleanup_expired_bags',
        'schedule': 3600,
        # 'schedule': 30, # For testing

    },
    
    'cleanup_expired_wishlists_task': {
        'task': 'src.wishlists.tasks.cleanup_expired_wishlists',
         'schedule': 3600,
        # 'schedule': 30, # For testing

    },
    'complete_old_orders_task': {
        'task': 'src.orders.tasks.complete_old_orders',
        'schedule': 3600,
        # 'schedule': 30, # For testing
    },
}
