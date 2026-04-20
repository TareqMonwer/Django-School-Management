"""
Custom Prometheus metrics per app and for SLO/SLA.

All metrics use the 'school' prefix (PROMETHEUS_METRIC_NAMESPACE) when
django_prometheus is configured with that namespace; otherwise use explicit prefix.
"""
from prometheus_client import Counter, Histogram, Gauge

# Map URL path prefixes to app labels (for per-app metrics)
API_APP_PREFIXES = (
    ("api/v1/students", "students"),
    ("api/v1/teachers", "teachers"),
    ("api/v1/academics", "academics"),
    ("api/v1/payments", "payments"),
    ("api/v1/articles", "articles"),
    ("account/", "accounts"),
    ("dashboard/", "dashboard"),
    ("students/", "students_site"),
    ("teachers/", "teachers_site"),
    ("academics/", "academics_site"),
    ("result/", "result"),
    ("institute/", "institute"),
    ("notices/", "notices"),
    ("blog/", "articles_site"),
)

# Per-app request count (method, status, app) - for SLO error rate by app
APP_REQUESTS_TOTAL = Counter(
    "school_app_requests_total",
    "Total HTTP requests per app",
    ["app", "method", "status"],
)

# Per-app request latency - for SLO latency (e.g. p99 < 500ms) by app
APP_REQUEST_DURATION_SECONDS = Histogram(
    "school_app_request_duration_seconds",
    "Request duration per app in seconds",
    ["app"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 10.0, float("inf")),
)

# Count of 5xx responses per app (for SLO availability)
APP_ERRORS_TOTAL = Counter(
    "school_app_errors_total",
    "Total 5xx responses per app",
    ["app"],
)

# Active requests in flight (gauge) - for capacity / saturation
APP_REQUESTS_IN_FLIGHT = Gauge(
    "school_app_requests_in_flight",
    "Number of requests currently being processed per app",
    ["app"],
)


def get_app_from_path(path):
    """Resolve app label from request path. Strips leading slash for matching."""
    p = path.lstrip("/")
    for prefix, app in API_APP_PREFIXES:
        if p.startswith(prefix):
            return app
    return "other"


def record_app_request(app, method, status_code, duration_seconds):
    """Record one request for per-app and SLO metrics."""
    status = str(status_code)
    APP_REQUESTS_TOTAL.labels(app=app, method=method, status=status).inc()
    APP_REQUEST_DURATION_SECONDS.labels(app=app).observe(duration_seconds)
    if 500 <= status_code < 600:
        APP_ERRORS_TOTAL.labels(app=app).inc()


def track_request_start(app):
    """Increment in-flight requests for app."""
    APP_REQUESTS_IN_FLIGHT.labels(app=app).inc()


def track_request_end(app):
    """Decrement in-flight requests for app."""
    APP_REQUESTS_IN_FLIGHT.labels(app=app).dec()
