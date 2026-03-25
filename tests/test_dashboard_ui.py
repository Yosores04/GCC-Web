from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from content.models import Page, PageSection


class DashboardUITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="staff-ui",
            password="pass12345",
            is_staff=True,
        )
        self.page = Page.objects.create(slug="about", title="About", is_published=True)
        self.section = PageSection.objects.create(
            page=self.page,
            section_key="section-1",
            heading="About Section 1",
            body="<p>Body</p>",
            display_order=1,
            is_active=True,
        )
        self.client.force_login(self.user)

    def test_dashboard_index_uses_dedicated_dashboard_theme(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/css/dashboard.css")
        self.assertContains(response, "dashboard-shell")
        self.assertContains(response, "dashboard-nav")

    def test_dashboard_uses_icon_markup(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "dash-link-icon")
        self.assertContains(response, "btn-icon")

    def test_section_edit_uses_form_card_layout(self):
        response = self.client.get(reverse("dashboard:section_edit", args=[self.section.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "editor-card")
        self.assertContains(response, "form-grid")
        self.assertContains(response, "Save changes")
