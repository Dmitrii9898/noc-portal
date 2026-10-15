from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import ROLE_STAFF, Role


class ExportTests(TestCase):
    def test_staff_downloads_xlsx(self):
        role, _ = Role.objects.get_or_create(name=ROLE_STAFF)
        get_user_model().objects.create_user(username="staff1", password="Secret#2025", role=role)
        self.client.login(username="staff1", password="Secret#2025")
        response = self.client.get("/office/reports/?format=xlsx")
        self.assertEqual(response.status_code, 200)
        self.assertIn("spreadsheetml", response["Content-Type"])
