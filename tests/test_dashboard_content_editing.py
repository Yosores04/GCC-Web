from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from content.models import GalleryImage, Page, PageSection


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

    def _upload_image(self, name, color):
        buffer = BytesIO()
        Image.new("RGB", (20, 20), color=color).save(buffer, format="PNG")
        return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")

    def test_staff_can_create_multiple_gallery_images_in_one_submit(self):
        url = reverse("dashboard:gallery_create")
        first = self._upload_image("first.png", (255, 0, 0))
        second = self._upload_image("second.png", (0, 255, 0))

        response = self.client.post(
            url,
            {
                "title": "Campus Life",
                "caption": "Batch upload",
                "category": "Events",
                "display_order": 2,
                "is_active": "on",
                "image": [first, second],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(GalleryImage.objects.count(), 2)

        items = list(GalleryImage.objects.order_by("display_order", "id"))
        self.assertEqual(items[0].title, "Campus Life")
        self.assertEqual(items[1].title, "Campus Life (2)")
