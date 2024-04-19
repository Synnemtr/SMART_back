from django.apps import AppConfig


class LogManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log_manager'

    def ready(self):
        from log_manager.log_updater import start
        start()
