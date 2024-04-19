from django.apps import AppConfig


class AppicationConfig(AppConfig):
    name = "app"

    def ready(self):
        import app.signals