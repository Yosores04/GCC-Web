from django.http import Http404
from django.shortcuts import render

from content.models import GalleryImage, Page

NAV_ITEMS = [
    {"label": "HOME", "url": "/"},
    {"label": "ABOUT", "url": "/about/"},
    {"label": "CONTACT", "url": "/contact/"},
    {"label": "COURSES", "url": "/courses/"},
    {"label": "ACTIVITIES", "url": "/activities/"},
    {"label": "GALLERY", "url": "/gallery/"},
]

PAGE_SECTION_LAYOUT = {
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

CAROUSEL_KEYS = {
    "home": ["hero-carousel", "program-highlights", "news-strip"],
    "activities": ["hero-banner", "activities-carousel", "student-life-grid"],
    "gallery": ["hero-banner", "gallery-carousel", "album-grid"],
}


def _get_page_or_404(slug):
    try:
        return Page.objects.get(slug=slug, is_published=True)
    except Page.DoesNotExist as exc:
        raise Http404("Page not found.") from exc


def _placeholder_section(slug, key):
    label = key.replace("-", " ").title()
    body = (
        f"<p>This {label} section is part of the {slug.title()} page blueprint. "
        "Update the heading, text, and image in the hidden dashboard.</p>"
    )
    return {
        "section_key": key,
        "heading": label,
        "body": body,
        "image_url": "",
    }


def _mapped_sections(page):
    keys = PAGE_SECTION_LAYOUT.get(page.slug, [])
    active_sections = {
        section.section_key: section
        for section in page.sections.active()
    }

    mapped = []
    for key in keys:
        section = active_sections.get(key)
        if section is None:
            mapped.append(_placeholder_section(page.slug, key))
            continue
        mapped.append(
            {
                "section_key": section.section_key,
                "heading": section.heading,
                "body": section.body,
                "image_url": section.image.url if section.image else "",
            }
        )
    return mapped


def _section_carousel(mapped_sections, page_slug):
    slide_keys = CAROUSEL_KEYS.get(page_slug, [])
    by_key = {section["section_key"]: section for section in mapped_sections}
    slides = []

    for key in slide_keys:
        section = by_key.get(key)
        if section and section.get("image_url"):
            slides.append(section)

    if len(slides) < 2:
        slides = [section for section in mapped_sections if section.get("image_url")][:3]
    if len(slides) < 2:
        slides = mapped_sections[:3]
    return slides


def _gallery_carousel(items, mapped_sections):
    slides = []
    for item in items[:5]:
        if item.image:
            slides.append(
                {
                    "section_key": f"gallery-item-{item.id}",
                    "heading": item.title,
                    "body": item.caption,
                    "image_url": item.image.url,
                }
            )
    if len(slides) >= 2:
        return slides
    return _section_carousel(mapped_sections, "gallery")


def home(request):
    page_obj = _get_page_or_404("home")
    mapped_sections = _mapped_sections(page_obj)
    carousel_slides = _section_carousel(mapped_sections, "home")
    context = {
        "page": page_obj,
        "mapped_sections": mapped_sections,
        "carousel_slides": carousel_slides,
        "nav_items": NAV_ITEMS,
    }
    return render(request, "website/home.html", context)


def page(request, slug):
    page_obj = _get_page_or_404(slug)
    mapped_sections = _mapped_sections(page_obj)
    carousel_slides = _section_carousel(mapped_sections, slug)
    context = {
        "page": page_obj,
        "mapped_sections": mapped_sections,
        "carousel_slides": carousel_slides,
        "nav_items": NAV_ITEMS,
    }
    return render(request, "website/page.html", context)


def gallery(request):
    page_obj = _get_page_or_404("gallery")
    mapped_sections = _mapped_sections(page_obj)
    items = GalleryImage.objects.filter(is_active=True).order_by("display_order", "id")
    carousel_slides = _gallery_carousel(list(items), mapped_sections)
    context = {
        "page": page_obj,
        "items": items,
        "mapped_sections": mapped_sections,
        "carousel_slides": carousel_slides,
        "nav_items": NAV_ITEMS,
    }
    return render(request, "website/gallery.html", context)
