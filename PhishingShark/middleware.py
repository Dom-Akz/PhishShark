# your_app/middleware.py
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForCaptureEndpoint(MiddlewareMixin):
    """Disable CSRF check for capture-credentials endpoint"""

    def process_request(self, request):
        if request.path == "/capture-credentials/":
            setattr(request, "_dont_enforce_csrf_checks", True)
        return None
