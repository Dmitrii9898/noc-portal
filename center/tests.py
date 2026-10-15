from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import ROLE_MEMBER, Role
from center.models import Direction, Event
from center.services import can_apply, submit_application


class ApplyRulesTests(TestCase):
    def setUp(self):
        role, _ = Role.objects.get_or_create(name=ROLE_MEMBER)
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="member1", password="x", role=role)
        direction = Direction.objects.create(code="4", title="Образование", slug="edu", summary="к", body="т")
        self.event = Event.objects.create(
            direction=direction, title="Семинар", slug="sem", place="Москва",
            starts_at=timezone.now(), summary="а", body="б", seats=1, is_open=True,
        )

    def test_no_seats(self):
        submit_application(self.user, "", None, event=self.event)
        other = get_user_model().objects.create_user(username="member2", password="x", role=self.user.role)
        self.assertIn("мест", can_apply(other, event=self.event))

    def test_already_applied(self):
        submit_application(self.user, "", None, event=self.event)
        self.assertIn("уже", can_apply(self.user, event=self.event).lower())
