from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from content.models import Page, PageSection, SiteSettings

PAGE_BLUEPRINT = {
    "home": {
        "title": "Home",
        "sections": [
            (
                "hero-carousel",
                "{school_name}",
                "<p>Empowering learners with values-driven and future-ready education.</p>",
            ),
            (
                "welcome-intro",
                "Welcome Message",
                "<p>Welcome to our official website. Edit this section with your principal's message.</p>",
            ),
            (
                "program-highlights",
                "Program Highlights",
                "<p>Showcase your top academic programs and student pathways here.</p>",
            ),
            (
                "news-strip",
                "Latest Campus News",
                "<p>Share announcements, achievements, and upcoming institutional events.</p>",
            ),
            (
                "cta-band",
                "Enroll With Us",
                "<p>Invite prospective students and families to connect with admissions.</p>",
            ),
        ],
    },
    "about": {
        "title": "About",
        "sections": [
            (
                "hero-banner",
                "About {school_name}",
                "<p>Introduce your institution's legacy and role in the community.</p>",
            ),
            (
                "institution-story",
                "Our Story",
                "<p>Describe your founding history and milestones.</p>",
            ),
            (
                "mission-vision",
                "Mission and Vision",
                "<p>Present your mission, vision, and core values.</p>",
            ),
            (
                "leadership-preview",
                "Leadership Team",
                "<p>Highlight school leaders and their commitment to student success.</p>",
            ),
            (
                "cta-band",
                "Join the School Community",
                "<p>Encourage prospective students to discover your programs.</p>",
            ),
        ],
    },
    "courses": {
        "title": "Courses",
        "sections": [
            (
                "hero-banner",
                "Academic Programs",
                "<p>Explore courses that prepare students for careers and lifelong learning.</p>",
            ),
            (
                "program-overview",
                "Program Overview",
                "<p>Provide an overview of your curriculum clusters and tracks.</p>",
            ),
            (
                "course-grid",
                "Course List",
                "<p>List key courses or departments available for enrollment.</p>",
            ),
            (
                "admissions-cta",
                "Admissions Information",
                "<p>Add entry requirements, schedules, and enrollment details.</p>",
            ),
            (
                "faq-teaser",
                "Frequently Asked Questions",
                "<p>Answer common questions from applicants and parents.</p>",
            ),
        ],
    },
    "activities": {
        "title": "Activities",
        "sections": [
            (
                "hero-banner",
                "Campus Activities",
                "<p>Show the vibrant student life and co-curricular culture at GCC.</p>",
            ),
            (
                "activities-carousel",
                "Featured Activities",
                "<p>Highlight sports, clubs, organizations, and special events.</p>",
            ),
            (
                "student-life-grid",
                "Student Life",
                "<p>Present student-led programs and achievements.</p>",
            ),
            (
                "events-teaser",
                "Upcoming Events",
                "<p>Promote upcoming school activities and celebrations.</p>",
            ),
            (
                "cta-band",
                "Be Part of Campus Life",
                "<p>Invite students to participate in organizations and programs.</p>",
            ),
        ],
    },
    "contact": {
        "title": "Contact",
        "sections": [
            (
                "hero-banner",
                "Contact Us",
                "<p>Reach out to {school_name} for inquiries and admissions support.</p>",
            ),
            (
                "contact-details",
                "Contact Details",
                "<p>Add your office phone numbers, emails, and operating hours.</p>",
            ),
            (
                "map-block",
                "Campus Location",
                "<p>Provide location details and commuting directions.</p>",
            ),
            (
                "inquiry-cta",
                "Inquiry Support",
                "<p>Guide visitors on how to send admissions and registrar questions.</p>",
            ),
            (
                "social-links",
                "Social Channels",
                "<p>Link official social media pages for updates.</p>",
            ),
        ],
    },
    "gallery": {
        "title": "Gallery",
        "sections": [
            (
                "hero-banner",
                "Campus Gallery",
                "<p>Discover photos of campus life, events, and academic programs.</p>",
            ),
            (
                "gallery-carousel",
                "Featured Moments",
                "<p>Use this section for top gallery highlights.</p>",
            ),
            (
                "album-grid",
                "Photo Albums",
                "<p>Curate themed albums such as academics, activities, and ceremonies.</p>",
            ),
            (
                "campus-life-text",
                "Campus Life",
                "<p>Share stories behind your photo highlights.</p>",
            ),
            (
                "cta-band",
                "Visit Our Campus",
                "<p>Invite visitors to tour the campus and learn more.</p>",
            ),
        ],
    },
}


def _with_school_name(text, school_name):
    return text.replace("{school_name}", school_name)


def _make_placeholder_image(page_slug, section_index, school_name):
    width, height = 1200, 700
    image = Image.new("RGB", (width, height), color=(231, 239, 249))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    title = f"{school_name} - {page_slug.title()} Section {section_index}"
    subtitle = "Placeholder image - replace from dashboard"

    draw.rectangle([(0, 0), (width, 110)], fill=(22, 58, 97))
    draw.text((42, 40), title, fill=(255, 255, 255), font=font)
    draw.text((42, 160), subtitle, fill=(17, 34, 58), font=font)
    draw.rectangle([(42, 210), (width - 42, height - 42)], outline=(88, 120, 156), width=3)

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class Command(BaseCommand):
    help = "Create initial pages for the GCC website."

    def handle(self, *args, **options):
        created = 0
        sections_created = 0
        school_name = SiteSettings.load().school_name or "Your School"

        for slug, blueprint in PAGE_BLUEPRINT.items():
            page, was_created = Page.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": blueprint["title"],
                    "is_published": True,
                },
            )
            if was_created:
                created += 1

            existing_by_key = {section.section_key: section for section in page.sections.all()}
            blueprint_keys = [item[0] for item in blueprint["sections"]]

            for section_index, (section_key, heading, body) in enumerate(blueprint["sections"], start=1):
                heading = _with_school_name(heading, school_name)
                body = _with_school_name(body, school_name)
                section = existing_by_key.get(section_key)
                section_created = False

                if section is None:
                    legacy_key = f"section-{section_index}"
                    legacy_section = existing_by_key.get(legacy_key)
                    if legacy_section and legacy_key not in blueprint_keys:
                        legacy_section.section_key = section_key
                        if not legacy_section.heading or legacy_section.heading.startswith(f"{page.title} Section"):
                            legacy_section.heading = heading
                        if not legacy_section.body or "placeholder content" in legacy_section.body.lower():
                            legacy_section.body = body
                        legacy_section.display_order = section_index
                        legacy_section.is_active = True
                        legacy_section.save()
                        section = legacy_section
                    else:
                        section, section_created = PageSection.objects.get_or_create(
                            page=page,
                            section_key=section_key,
                            defaults={
                                "heading": heading,
                                "body": body,
                                "display_order": section_index,
                                "is_active": True,
                            },
                        )
                else:
                    changed = False
                    if not section.heading:
                        section.heading = heading
                        changed = True
                    if not section.body:
                        section.body = body
                        changed = True
                    if section.display_order != section_index:
                        section.display_order = section_index
                        changed = True
                    if not section.is_active:
                        section.is_active = True
                        changed = True
                    if changed:
                        section.save()

                if section_created:
                    sections_created += 1

                if not section.image:
                    safe_key = section_key.replace("_", "-")
                    filename = f"{slug}-{safe_key}.png"
                    image_bytes = _make_placeholder_image(slug, section_index, school_name)
                    section.image.save(f"placeholders/{filename}", ContentFile(image_bytes), save=True)

        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete. "
                f"Created {created} page(s), {sections_created} section(s), and ensured placeholders."
            )
        )
