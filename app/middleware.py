from django.contrib.auth import logout
from app import settings
import time


class SessionSecurityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        # if user and user.is_authenticated and not user.is_superuser and user.has_session_force_timeout:
        if user and user.is_authenticated and not user.is_superuser:
            now = time.time()
            try:
                last_activity = request.session['last_activity']
            except KeyError:
                last_activity = now
            if time.time() - last_activity > getattr(settings, 'SESSION_AUTO_TIMEOUT_AGE', 600):
                logout(request)
            else:
                request.session['last_activity'] = now
        response = self.get_response(request)
        return response
