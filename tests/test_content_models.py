from django.test import TestCase

from content.models import Page, PageSection


class PageSectionOrderingTests(TestCase):
    def test_sections_returned_in_display_order(self):
        page = Page.objects.create(slug="about", title="About", is_published=True)
        PageSection.objects.create(
            page=page,
            section_key="later",
            heading="Later",
            display_order=2,
            is_active=True,
        )
        PageSection.objects.create(
            page=page,
            section_key="first",
            heading="First",
            display_order=1,
            is_active=True,
        )

        keys = list(page.sections.active().values_list("section_key", flat=True))
        self.assertEqual(keys, ["first", "later"])
