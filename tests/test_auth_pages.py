from django.test import TestCase
from django.urls import reverse

from content.models import SiteSettings


class AuthPageTests(TestCase):
    def test_login_page_uses_modern_layout(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "auth-shell")
        self.assertContains(response, "auth-card")
        self.assertContains(response, "Sign in to continue")

    def test_login_page_preserves_next_parameter(self):
        response = self.client.get(f"{reverse('login')}?next=/control-room-2026/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="next"')
        self.assertContains(response, 'value="/control-room-2026/"')

    def test_login_page_copy_uses_site_school_name(self):
        settings_obj = SiteSettings.load()
        settings_obj.school_name = "North Valley College"
        settings_obj.save(update_fields=["school_name"])

        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "North Valley College website")
