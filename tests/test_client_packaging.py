from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from content.models import GalleryImage, Page, PageSection, SiteSettings


class ClientPackagingTests(TestCase):
    def test_site_settings_has_extended_branding_fields(self):
        field_names = {field.name for field in SiteSettings._meta.get_fields()}
        self.assertIn("tagline", field_names)
        self.assertIn("website_url", field_names)
        self.assertIn("admissions_url", field_names)
        self.assertIn("instagram_url", field_names)
        self.assertIn("youtube_url", field_names)
        self.assertIn("map_embed_url", field_names)

    def test_onboard_new_client_resets_content_and_seeds_blueprint(self):
        page = Page.objects.create(slug="legacy-page", title="Legacy", is_published=True)
        PageSection.objects.create(
            page=page,
            section_key="legacy",
            heading="Legacy heading",
            body="Legacy body",
            display_order=1,
            is_active=True,
        )
        GalleryImage.objects.create(
            title="Legacy Photo",
            caption="Legacy",
            image="gallery/legacy.png",
            display_order=1,
            is_active=True,
        )

        call_command(
            "onboard_new_client",
            "--school-name",
            "Demo Academy",
            "--tagline",
            "Future-ready learning",
            "--contact-email",
            "hello@demo.edu",
        )

        settings_obj = SiteSettings.load()
        self.assertEqual(settings_obj.school_name, "Demo Academy")
        self.assertEqual(settings_obj.tagline, "Future-ready learning")
        self.assertEqual(settings_obj.contact_email, "hello@demo.edu")
        self.assertEqual(Page.objects.count(), 6)
        self.assertEqual(PageSection.objects.count(), 30)
        self.assertEqual(GalleryImage.objects.count(), 0)
        self.assertFalse(Page.objects.filter(slug="legacy-page").exists())

    def test_export_then_import_restores_site_content(self):
        settings_obj = SiteSettings.load()
        settings_obj.school_name = "Export Academy"
        settings_obj.tagline = "Build your future"
        settings_obj.contact_email = "info@export.edu"
        settings_obj.contact_phone = "+63 999 111 2222"
        settings_obj.address = "Export City"
        settings_obj.facebook_url = "https://facebook.com/exportacademy"
        settings_obj.website_url = "https://export.edu"
        settings_obj.admissions_url = "https://export.edu/admissions"
        settings_obj.instagram_url = "https://instagram.com/exportacademy"
        settings_obj.youtube_url = "https://youtube.com/exportacademy"
        settings_obj.map_embed_url = "https://maps.example/embed/export"
        settings_obj.save()

        page = Page.objects.create(slug="about", title="About", is_published=True)
        PageSection.objects.create(
            page=page,
            section_key="institution-story",
            heading="Our Story",
            body="<p>Export body</p>",
            image="sections/about-story.png",
            display_order=1,
            is_active=True,
        )
        GalleryImage.objects.create(
            title="Campus",
            caption="Export campus",
            category="Campus",
            image="gallery/export-campus.png",
            display_order=1,
            is_active=True,
        )

        export_path = Path("tmp-client-package-test.json")
        try:
            call_command("export_site_content", str(export_path))

            PageSection.objects.all().delete()
            Page.objects.all().delete()
            GalleryImage.objects.all().delete()
            settings_obj = SiteSettings.load()
            settings_obj.school_name = "Changed Name"
            settings_obj.tagline = ""
            settings_obj.contact_email = ""
            settings_obj.save()

            call_command("import_site_content", str(export_path))
        finally:
            if export_path.exists():
                export_path.unlink()

        restored_settings = SiteSettings.load()
        self.assertEqual(restored_settings.school_name, "Export Academy")
        self.assertEqual(restored_settings.tagline, "Build your future")
        self.assertEqual(restored_settings.website_url, "https://export.edu")
        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(PageSection.objects.count(), 1)
        self.assertEqual(GalleryImage.objects.count(), 1)
