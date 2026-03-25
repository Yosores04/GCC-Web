from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from content.models import Page, SiteSettings


class PublicPageTests(TestCase):
    def setUp(self):
        Page.objects.create(slug="home", title="Home", is_published=True)
        Page.objects.create(slug="about", title="About", is_published=True)
        Page.objects.create(slug="contact", title="Contact", is_published=True)
        Page.objects.create(slug="courses", title="Courses", is_published=True)
        Page.objects.create(slug="activities", title="Activities", is_published=True)
        Page.objects.create(slug="gallery", title="Gallery", is_published=True)

    def test_home_page_renders_and_shows_navigation(self):
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HOME")
        self.assertContains(response, "ABOUT")
        self.assertContains(response, "CONTACT")
        self.assertContains(response, "COURSES")
        self.assertContains(response, "ACTIVITIES")
        self.assertContains(response, "GALLERY")

    def test_home_page_uses_modern_layout_markup(self):
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="site-header"')
        self.assertContains(response, 'class="top-nav"')
        self.assertContains(response, "content-card")
        self.assertContains(response, "/static/css/site.css")

    def test_home_page_has_live_carousel_markup(self):
        call_command("seed_initial_content")
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-carousel")
        self.assertContains(response, "carousel-track")
        self.assertContains(response, "carousel-slide")

    def test_activities_page_has_live_carousel_markup(self):
        call_command("seed_initial_content")
        response = self.client.get(reverse("website:activities"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-carousel")

    def test_gallery_page_has_live_carousel_markup(self):
        call_command("seed_initial_content")
        response = self.client.get(reverse("website:gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-carousel")

    def test_header_shows_uploaded_site_logo(self):
        site_settings = SiteSettings.load()
        site_settings.logo = "site/school-logo.png"
        site_settings.save(update_fields=["logo"])

        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="brand-logo"')
        self.assertContains(response, "/media/site/school-logo.png")

    def test_footer_uses_site_settings_details(self):
        site_settings = SiteSettings.load()
        site_settings.contact_email = "info@gcc.edu.ph"
        site_settings.contact_phone = "+63 88 123 4567"
        site_settings.address = "Gingoog City, Misamis Oriental"
        site_settings.facebook_url = "https://facebook.com/gingoogcitycolleges"
        site_settings.save(
            update_fields=["contact_email", "contact_phone", "address", "facebook_url"]
        )

        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="site-footer"')
        self.assertContains(response, "info@gcc.edu.ph")
        self.assertContains(response, "+63 88 123 4567")
        self.assertContains(response, "Gingoog City, Misamis Oriental")
        self.assertContains(response, "https://facebook.com/gingoogcitycolleges")

    def test_head_uses_uploaded_logo_as_favicon(self):
        site_settings = SiteSettings.load()
        site_settings.logo = "site/gcc-logo-tab.png"
        site_settings.save(update_fields=["logo"])

        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="icon"')
        self.assertContains(response, "/media/site/gcc-logo-tab.png")

    def test_footer_uses_compact_layout_class(self):
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="footer-shell footer-shell-compact"')

    def test_footer_has_icon_markup(self):
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "site-icon-sprite")
        self.assertContains(response, "footer-icon")

    def test_school_name_is_used_in_public_page_title_and_hero_label(self):
        site_settings = SiteSettings.load()
        site_settings.school_name = "North Valley College"
        site_settings.save(update_fields=["school_name"])

        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Home | North Valley College</title>", html=True)
        self.assertContains(response, '<p class="eyebrow">North Valley College</p>', html=True)
