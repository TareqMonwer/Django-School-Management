"""Views for health check (readiness/liveness)."""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.cache import cache


@csrf_exempt
@require_GET
@never_cache
def health_view(request):
    """
    Health check for load balancers and Kubernetes.
    Returns 200 if DB and cache are reachable, 503 otherwise.
    """
    status = "ok"
    code = 200
    checks = {}

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = str(e)
        status = "degraded"
        code = 503

    try:
        cache.set("health_check", 1, timeout=5)
        if cache.get("health_check") != 1:
            raise Exception("cache read/write failed")
        checks["cache"] = "ok"
    except Exception as e:
        checks["cache"] = str(e)
        status = "degraded"
        code = 503

    return JsonResponse({"status": status, "checks": checks}, status=code)
