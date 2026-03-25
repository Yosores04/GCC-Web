from django.core.management import call_command
from django.test import TestCase

from content.models import Page, PageSection

SECTION_BLUEPRINT = {
    "home": [
        "hero-carousel",
        "welcome-intro",
        "program-highlights",
        "news-strip",
        "cta-band",
    ],
    "about": [
        "hero-banner",
        "institution-story",
        "mission-vision",
        "leadership-preview",
        "cta-band",
    ],
    "courses": [
        "hero-banner",
        "program-overview",
        "course-grid",
        "admissions-cta",
        "faq-teaser",
    ],
    "activities": [
        "hero-banner",
        "activities-carousel",
        "student-life-grid",
        "events-teaser",
        "cta-band",
    ],
    "contact": [
        "hero-banner",
        "contact-details",
        "map-block",
        "inquiry-cta",
        "social-links",
    ],
    "gallery": [
        "hero-banner",
        "gallery-carousel",
        "album-grid",
        "campus-life-text",
        "cta-band",
    ],
}


class SeedCommandTests(TestCase):
    def test_seed_creates_required_pages(self):
        call_command("seed_initial_content")

        for slug in SECTION_BLUEPRINT:
            self.assertTrue(Page.objects.filter(slug=slug).exists())

    def test_seed_creates_mapped_placeholder_sections_with_images_per_page(self):
        call_command("seed_initial_content")

        for slug, expected_keys in SECTION_BLUEPRINT.items():
            page = Page.objects.get(slug=slug)
            sections = list(page.sections.order_by("display_order", "id"))
            self.assertEqual(len(sections), len(expected_keys))

            for index, (section, expected_key) in enumerate(zip(sections, expected_keys), start=1):
                self.assertEqual(section.section_key, expected_key)
                self.assertTrue(section.heading)
                self.assertTrue(section.body)
                self.assertEqual(section.display_order, index)
                self.assertTrue(section.is_active)
                self.assertTrue(section.image)

    def test_seed_is_idempotent_for_sections(self):
        call_command("seed_initial_content")
        call_command("seed_initial_content")

        total_sections = PageSection.objects.count()
        # 6 pages * 5 sections each
        self.assertEqual(total_sections, 30)
