from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = "api.authentication"

    def ready(self):
        import app.signals
