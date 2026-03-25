from django.contrib import admin

from .models import GalleryImage, Page, PageSection, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("school_name", "contact_email", "contact_phone", "updated_at")
    fieldsets = (
        (
            "Branding",
            {
                "fields": ("school_name", "tagline", "logo"),
            },
        ),
        (
            "Contact",
            {
                "fields": ("contact_email", "contact_phone", "address", "map_embed_url"),
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "website_url",
                    "admissions_url",
                    "facebook_url",
                    "instagram_url",
                    "youtube_url",
                ),
            },
        ),
    )


class PageSectionInline(admin.TabularInline):
    model = PageSection
    extra = 1
    fields = ("section_key", "heading", "display_order", "is_active")
    ordering = ("display_order", "id")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("slug", "title")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageSectionInline]


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ("page", "section_key", "heading", "display_order", "is_active")
    list_filter = ("page", "is_active")
    search_fields = ("section_key", "heading", "page__title")
    ordering = ("page", "display_order", "id")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "display_order", "is_active", "updated_at")
    list_filter = ("is_active", "category")
    search_fields = ("title", "category", "caption")
    ordering = ("display_order", "id")
