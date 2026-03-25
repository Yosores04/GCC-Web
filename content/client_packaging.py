import json
from datetime import datetime, timezone
from pathlib import Path

from django.db import transaction

from .models import GalleryImage, Page, PageSection, SiteSettings

SITE_SETTINGS_FIELDS = [
    "school_name",
    "tagline",
    "contact_email",
    "contact_phone",
    "address",
    "facebook_url",
    "instagram_url",
    "youtube_url",
    "website_url",
    "admissions_url",
    "map_embed_url",
]

PAGE_FIELDS = [
    "slug",
    "title",
    "meta_title",
    "meta_description",
    "is_published",
]

SECTION_FIELDS = [
    "section_key",
    "heading",
    "body",
    "display_order",
    "is_active",
]

GALLERY_FIELDS = [
    "title",
    "caption",
    "category",
    "display_order",
    "is_active",
]


def build_export_payload():
    settings_obj = SiteSettings.load()
    settings_data = {field: getattr(settings_obj, field, "") for field in SITE_SETTINGS_FIELDS}
    settings_data["logo"] = settings_obj.logo.name if settings_obj.logo else ""

    pages_data = []
    for page in Page.objects.all().order_by("id"):
        page_data = {field: getattr(page, field) for field in PAGE_FIELDS}
        sections_data = []
        for section in page.sections.all().order_by("display_order", "id"):
            section_data = {field: getattr(section, field) for field in SECTION_FIELDS}
            section_data["image"] = section.image.name if section.image else ""
            sections_data.append(section_data)
        page_data["sections"] = sections_data
        pages_data.append(page_data)

    gallery_data = []
    for item in GalleryImage.objects.all().order_by("display_order", "id"):
        entry = {field: getattr(item, field) for field in GALLERY_FIELDS}
        entry["image"] = item.image.name if item.image else ""
        gallery_data.append(entry)

    return {
        "version": 1,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "site_settings": settings_data,
        "pages": pages_data,
        "gallery": gallery_data,
    }


def write_payload_to_file(payload, output_path):
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return destination


def read_payload_from_file(input_path):
    source = Path(input_path)
    return json.loads(source.read_text(encoding="utf-8"))


def apply_import_payload(payload, reset_existing=True):
    with transaction.atomic():
        if reset_existing:
            PageSection.objects.all().delete()
            Page.objects.all().delete()
            GalleryImage.objects.all().delete()

        settings_obj = SiteSettings.load()
        settings_data = payload.get("site_settings", {})
        for field in SITE_SETTINGS_FIELDS:
            setattr(settings_obj, field, settings_data.get(field, ""))
        settings_obj.logo = settings_data.get("logo", "") or None
        settings_obj.save()

        pages_written = 0
        sections_written = 0
        gallery_written = 0

        for page_data in payload.get("pages", []):
            slug = (page_data.get("slug") or "").strip()
            if not slug:
                continue

            page, _ = Page.objects.get_or_create(slug=slug)
            page.title = page_data.get("title", slug.replace("-", " ").title())
            page.meta_title = page_data.get("meta_title", "")
            page.meta_description = page_data.get("meta_description", "")
            page.is_published = bool(page_data.get("is_published", True))
            page.save()
            pages_written += 1

            if reset_existing:
                page.sections.all().delete()

            seen_keys = set()
            for section_data in page_data.get("sections", []):
                section_key = (section_data.get("section_key") or "").strip()
                if not section_key or section_key in seen_keys:
                    continue
                seen_keys.add(section_key)

                if reset_existing:
                    section = PageSection(page=page, section_key=section_key)
                else:
                    section, _ = PageSection.objects.get_or_create(
                        page=page,
                        section_key=section_key,
                    )

                section.heading = section_data.get("heading", "")
                section.body = section_data.get("body", "")
                section.display_order = int(section_data.get("display_order", 1) or 1)
                section.is_active = bool(section_data.get("is_active", True))
                section.image = section_data.get("image", "") or None
                section.save()
                sections_written += 1

        if not reset_existing:
            existing_gallery = set(
                GalleryImage.objects.values_list("title", "display_order")
            )
        else:
            existing_gallery = set()

        for item_data in payload.get("gallery", []):
            image_path = (item_data.get("image") or "").strip()
            if not image_path:
                continue

            title = (item_data.get("title") or "").strip() or "Untitled"
            display_order = int(item_data.get("display_order", 1) or 1)
            key = (title, display_order)

            if not reset_existing and key in existing_gallery:
                item = GalleryImage.objects.get(title=title, display_order=display_order)
            else:
                item = GalleryImage(title=title, display_order=display_order)

            item.caption = item_data.get("caption", "")
            item.category = item_data.get("category", "")
            item.is_active = bool(item_data.get("is_active", True))
            item.image = image_path
            item.save()
            gallery_written += 1

            if not reset_existing:
                existing_gallery.add(key)

    return {
        "pages_written": pages_written,
        "sections_written": sections_written,
        "gallery_written": gallery_written,
    }
