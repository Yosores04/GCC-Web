from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardPermissionTests(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)

    def test_non_staff_forbidden(self):
        user = get_user_model().objects.create_user(
            username="nonstaff",
            password="pass12345",
            is_staff=False,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 403)

    def test_staff_allowed(self):
        user = get_user_model().objects.create_user(
            username="staff",
            password="pass12345",
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
