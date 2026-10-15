from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import ROLE_MEMBER, Role


class MemberAccessTests(TestCase):
    def test_member_cannot_open_office(self):
        role, _ = Role.objects.get_or_create(name=ROLE_MEMBER)
        get_user_model().objects.create_user(username="member1", password="Secret#2025", role=role)
        self.client.login(username="member1", password="Secret#2025")
        response = self.client.get("/office/")
        self.assertEqual(response.status_code, 403)
