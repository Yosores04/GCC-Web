from django.conf import settings
from django.db import models

from ckeditor.fields import RichTextField


class ActiveSectionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True).order_by("display_order", "id")


class SiteSettings(models.Model):
    school_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    admissions_url = models.URLField(blank=True)
    map_embed_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        instance, _ = cls.objects.get_or_create(
            pk=1,
            defaults={"school_name": "Gingoog City Colleges"},
        )
        return instance

    def __str__(self):
        return self.school_name


class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["title", "id"]

    def __str__(self):
        return self.title


class PageSection(models.Model):
    page = models.ForeignKey(Page, related_name="sections", on_delete=models.CASCADE)
    section_key = models.SlugField(max_length=60)
    heading = models.CharField(max_length=200, blank=True)
    body = RichTextField(blank=True)
    image = models.ImageField(upload_to="sections/", blank=True, null=True)
    display_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = ActiveSectionQuerySet.as_manager()

    class Meta:
        ordering = ["display_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["page", "section_key"],
                name="unique_section_key_per_page",
            )
        ]

    def __str__(self):
        return f"{self.page.slug}:{self.section_key}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery/")
    display_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title
