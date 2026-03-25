from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from content.models import Page, PageSection


class DashboardContentEditingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="staff",
            password="pass12345",
            is_staff=True,
        )
        self.page = Page.objects.create(slug="about", title="About", is_published=True)
        self.section = PageSection.objects.create(
            page=self.page,
            section_key="intro",
            heading="Old heading",
            body="Old body",
            display_order=1,
            is_active=True,
        )
        self.client.force_login(self.user)

    def test_staff_can_update_section_text(self):
        url = reverse("dashboard:section_edit", args=[self.section.id])
        response = self.client.post(
            url,
            {
                "heading": "New heading",
                "body": "<p>Updated body</p>",
                "display_order": 1,
                "is_active": True,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.section.refresh_from_db()
        self.assertEqual(self.section.heading, "New heading")
