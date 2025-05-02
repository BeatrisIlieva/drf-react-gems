from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_ts_gems.accounts'

    def ready(self):
        import django_ts_gems.accounts.signals
