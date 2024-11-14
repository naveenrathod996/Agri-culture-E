from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                idle_duration = timezone.now() - last_activity
                if idle_duration > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    request.session.flush()  # Expire the session
                    return redirect('login')  # Redirect to login page

            request.session['last_activity'] = timezone.now()

        response = self.get_response(request)
        return response
