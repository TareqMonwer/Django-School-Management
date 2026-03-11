import os
import re
from urllib.parse import urlencode

from locust import HttpUser, task, between


DJANGO_HOST = os.environ.get("DJANGO_HOST", "http://web:8000")
STAFF_USERNAME = os.environ.get("PERF_STAFF_USERNAME", "perf_admin")
STAFF_PASSWORD = os.environ.get("PERF_STAFF_PASSWORD", "perf_admin")

# For admission_confirmation filtering; must exist in DB (from seed_performance_data).
PERF_DEPARTMENT_ID = os.environ.get("PERF_DEPARTMENT_ID", "1")
PERF_BATCH_ID = os.environ.get("PERF_BATCH_ID", "1")


def extract_csrf(html: str) -> str | None:
    """
    Extract CSRF token from a Django form using a simple regex.
    """
    match = re.search(
        r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', html
    )
    return match.group(1) if match else None


class AuthenticatedStaffUser(HttpUser):
    """
    Represents an admin/academic_officer visiting dashboards and admission pages.
    """

    wait_time = between(1, 5)

    def on_start(self):
        # Base URL is controlled via DJANGO_HOST, useful for Docker setups.
        self.client.base_url = DJANGO_HOST
        self._login()

    def _login(self):
        # allauth default login URL; adjust if your setup differs.
        login_path = "/accounts/login/"
        resp = self.client.get(login_path, name="login_page")
        token = extract_csrf(resp.text) or ""

        payload = {
            "login": STAFF_USERNAME,
            "password": STAFF_PASSWORD,
            "csrfmiddlewaretoken": token,
        }
        headers = {"Referer": login_path}
        r = self.client.post(
            login_path,
            data=payload,
            headers=headers,
            name="login_submit",
            allow_redirects=True,
        )
        if r.status_code >= 400:
            r.failure(f"Login failed: {r.status_code}")

    @task(3)
    def dashboard_home(self):
        # Staff dashboard home
        self.client.get("/dashboard/", name="dashboard_home")

    @task(3)
    def students_dashboard(self):
        # Students admission dashboard index
        self.client.get("/students/", name="students_dashboard")

    @task(2)
    def admitted_students_list(self):
        # List of admitted students from online registration
        self.client.get("/students/admitted-students/", name="admitted_students")

    @task(2)
    def admission_confirmation_page(self):
        # Bulk admission confirmation page, filtered by department and batch
        params = {
            "department_id": PERF_DEPARTMENT_ID,
            "batch_id": PERF_BATCH_ID,
        }
        path = f"/students/admission-confirm/?{urlencode(params)}"
        self.client.get(path, name="admission_confirmation_get")


class PublicApplicantUser(HttpUser):
    """
    Simulates unauthenticated applicants browsing the online admission page.
    """

    wait_time = between(1, 5)

    def on_start(self):
        self.client.base_url = DJANGO_HOST

    @task(5)
    def online_admission_page(self):
        self.client.get("/admission/", name="online_admission")

