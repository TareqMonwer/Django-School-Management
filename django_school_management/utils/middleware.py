"""Middleware for per-app and SLO metrics."""
import time
from django.utils.deprecation import MiddlewareMixin

from .metrics import get_app_from_path, record_app_request, track_request_end, track_request_start


class AppMetricsMiddleware(MiddlewareMixin):
    """
    Records per-app metrics and SLO-related metrics (request count, duration, errors).
    Must run after PrometheusAfterMiddleware so we have the full request.
    """

    def process_request(self, request):
        request._app_metrics_start = time.time()
        request._app_metrics_app = get_app_from_path(request.path)
        track_request_start(request._app_metrics_app)
        return None

    def process_response(self, request, response):
        if hasattr(request, "_app_metrics_start") and hasattr(request, "_app_metrics_app"):
            duration = time.time() - request._app_metrics_start
            app = request._app_metrics_app
            record_app_request(app, request.method, response.status_code, duration)
            track_request_end(app)
        return response
