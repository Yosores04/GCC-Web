# GCC Website + Secret Dashboard Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Django website with editable text/images, a hidden staff dashboard, and retained `/admin/` access.

**Architecture:** Create a Django project with three apps (`website`, `content`, `dashboard`). Store editable page sections and gallery images in `content` models, render them on public routes from `website`, and manage them through a hidden authenticated editor UI in `dashboard`.

**Tech Stack:** Python 3.12+, Django 5.x, django-ckeditor, Pillow, SQLite (dev), Django test framework.

---

### Task 1: Project Bootstrap (Config Exception to TDD)

**Files:**
- Create: `requirements.txt`
- Create: `manage.py`
- Create: `config/__init__.py`
- Create: `config/settings.py`
- Create: `config/urls.py`
- Create: `config/wsgi.py`
- Create: `config/asgi.py`
- Create: `.env.example`

**Step 1: Create dependency file**

```txt
Django>=5.0,<6.0
django-ckeditor>=6.7.0,<7.0
Pillow>=10.0,<11.0
python-dotenv>=1.0,<2.0
```

**Step 2: Install dependencies**

Run: `pip install -r requirements.txt`  
Expected: installs Django, ckeditor, Pillow, dotenv without errors.

**Step 3: Scaffold project**

Run: `django-admin startproject config .`  
Expected: creates `manage.py` and `config/*`.

**Step 4: Add environment template**

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_DASHBOARD_PATH=control-room-2026/
```

**Step 5: Commit**

```bash
git add requirements.txt .env.example manage.py config
git commit -m "chore: bootstrap django project and base settings"
```

### Task 2: Settings and URL Foundation

**Files:**
- Modify: `config/settings.py`
- Modify: `config/urls.py`
- Create: `templates/base.html`
- Create: `templates/403.html`
- Create: `templates/404.html`
- Create: `templates/registration/login.html`
- Create: `tests/test_settings_and_urls.py`

**Step 1: Write the failing test**

```python
from django.conf import settings
from django.test import SimpleTestCase


class SettingsAndURLTests(SimpleTestCase):
    def test_secret_dashboard_path_defined(self):
        self.assertTrue(hasattr(settings, "SECRET_DASHBOARD_PATH"))
        self.assertTrue(settings.SECRET_DASHBOARD_PATH.endswith("/"))
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_settings_and_urls.py -v 2`  
Expected: FAIL because `SECRET_DASHBOARD_PATH` is missing.

**Step 3: Write minimal implementation**

Add to `config/settings.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_DASHBOARD_PATH = os.getenv("SECRET_DASHBOARD_PATH", "control-room-2026/")

INSTALLED_APPS += [
    "ckeditor",
]

TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
```

Update `config/urls.py` to include:

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_settings_and_urls.py -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add config/settings.py config/urls.py templates tests/test_settings_and_urls.py
git commit -m "feat: configure env-driven secret dashboard path and media settings"
```

### Task 3: Create Apps and Core Content Models

**Files:**
- Create: `content/apps.py`
- Create: `content/models.py`
- Create: `content/admin.py`
- Create: `content/migrations/__init__.py`
- Create: `website/apps.py`
- Create: `dashboard/apps.py`
- Create: `tests/test_content_models.py`

**Step 1: Write the failing test**

```python
from django.test import TestCase
from content.models import Page, PageSection


class PageSectionOrderingTests(TestCase):
    def test_sections_returned_in_display_order(self):
        page = Page.objects.create(slug="about", title="About", is_published=True)
        PageSection.objects.create(page=page, section_key="b", heading="B", display_order=2, is_active=True)
        PageSection.objects.create(page=page, section_key="a", heading="A", display_order=1, is_active=True)
        keys = list(page.sections.active().values_list("section_key", flat=True))
        self.assertEqual(keys, ["a", "b"])
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_content_models.py -v 2`  
Expected: FAIL with `ModuleNotFoundError: No module named 'content'`.

**Step 3: Write minimal implementation**

Create apps:

```bash
python manage.py startapp content
python manage.py startapp website
python manage.py startapp dashboard
```

Add apps to `INSTALLED_APPS`:

```python
"content",
"website",
"dashboard",
```

Implement `content/models.py`:

```python
from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField


class ActiveSectionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True).order_by("display_order", "id")


class SiteSettings(models.Model):
    school_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    facebook_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"school_name": "Gingoog City Colleges"})
        return obj


class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

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
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    objects = ActiveSectionQuerySet.as_manager()

    class Meta:
        ordering = ["display_order", "id"]
        unique_together = ("page", "section_key")


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery/")
    display_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["display_order", "id"]
```

Run migrations:

```bash
python manage.py makemigrations content
python manage.py migrate
```

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_content_models.py -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add config/settings.py content website dashboard tests/test_content_models.py
git commit -m "feat: add content models for pages sections and gallery"
```

### Task 4: Public Website Views and Navigation

**Files:**
- Create: `website/views.py`
- Create: `website/urls.py`
- Create: `templates/website/home.html`
- Create: `templates/website/page.html`
- Create: `templates/website/gallery.html`
- Create: `tests/test_public_pages.py`
- Modify: `templates/base.html`
- Modify: `config/urls.py`

**Step 1: Write the failing test**

```python
from django.test import TestCase
from django.urls import reverse
from content.models import Page


class PublicPageTests(TestCase):
    def setUp(self):
        Page.objects.create(slug="home", title="Home", is_published=True)
        Page.objects.create(slug="about", title="About", is_published=True)

    def test_home_page_renders(self):
        response = self.client.get(reverse("website:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HOME")
        self.assertContains(response, "ABOUT")
        self.assertContains(response, "CONTACT")
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_public_pages.py -v 2`  
Expected: FAIL because `website` URLs/views do not exist.

**Step 3: Write minimal implementation**

Create `website/urls.py` with named routes:

```python
from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.page, {"slug": "about"}, name="about"),
    path("contact/", views.page, {"slug": "contact"}, name="contact"),
    path("courses/", views.page, {"slug": "courses"}, name="courses"),
    path("activities/", views.page, {"slug": "activities"}, name="activities"),
    path("gallery/", views.gallery, name="gallery"),
]
```

Create `website/views.py`:

```python
from django.http import Http404
from django.shortcuts import render
from content.models import GalleryImage, Page

NAV_ITEMS = [
    ("HOME", "/"),
    ("ABOUT", "/about/"),
    ("CONTACT", "/contact/"),
    ("COURSES", "/courses/"),
    ("ACTIVITIES", "/activities/"),
    ("GALLERY", "/gallery/"),
]


def _get_page_or_404(slug):
    try:
        return Page.objects.get(slug=slug, is_published=True)
    except Page.DoesNotExist as exc:
        raise Http404 from exc


def home(request):
    page = _get_page_or_404("home")
    sections = page.sections.active()
    return render(request, "website/home.html", {"page": page, "sections": sections, "nav_items": NAV_ITEMS})


def page(request, slug):
    page_obj = _get_page_or_404(slug)
    sections = page_obj.sections.active()
    return render(request, "website/page.html", {"page": page_obj, "sections": sections, "nav_items": NAV_ITEMS})


def gallery(request):
    items = GalleryImage.objects.filter(is_active=True).order_by("display_order", "id")
    return render(request, "website/gallery.html", {"items": items, "nav_items": NAV_ITEMS})
```

Update `config/urls.py`:

```python
path("", include("website.urls")),
```

Update `templates/base.html` with navigation matching provided design:

```html
<nav class="main-nav">
  {% for label, href in nav_items %}
    <a href="{{ href }}">{{ label }}</a>{% if not forloop.last %}<span>/</span>{% endif %}
  {% endfor %}
</nav>
```

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_public_pages.py -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add website templates/website templates/base.html config/urls.py tests/test_public_pages.py
git commit -m "feat: add public website pages and top navigation"
```

### Task 5: Hidden Dashboard Access Control

**Files:**
- Create: `dashboard/views.py`
- Create: `dashboard/urls.py`
- Create: `dashboard/forms.py`
- Create: `templates/dashboard/index.html`
- Create: `tests/test_dashboard_permissions.py`
- Modify: `config/urls.py`

**Step 1: Write the failing test**

```python
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardPermissionTests(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)

    def test_non_staff_forbidden(self):
        user = get_user_model().objects.create_user(username="u1", password="pass12345")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 403)

    def test_staff_allowed(self):
        user = get_user_model().objects.create_user(
            username="staff", password="pass12345", is_staff=True
        )
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_dashboard_permissions.py -v 2`  
Expected: FAIL because dashboard routes/views do not exist.

**Step 3: Write minimal implementation**

`dashboard/views.py`:

```python
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


def _is_editor(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(_is_editor)
def index(request):
    return render(request, "dashboard/index.html")
```

`dashboard/urls.py`:

```python
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
]
```

`config/urls.py`:

```python
from django.conf import settings
...
path(settings.SECRET_DASHBOARD_PATH, include("dashboard.urls")),
```

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_dashboard_permissions.py -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add dashboard config/urls.py templates/dashboard/index.html tests/test_dashboard_permissions.py
git commit -m "feat: add hidden staff-only dashboard route and access controls"
```

### Task 6: Dashboard Content Editing (Text + Images)

**Files:**
- Modify: `dashboard/views.py`
- Modify: `dashboard/forms.py`
- Modify: `dashboard/urls.py`
- Create: `templates/dashboard/page_list.html`
- Create: `templates/dashboard/section_form.html`
- Create: `templates/dashboard/gallery_list.html`
- Create: `templates/dashboard/gallery_form.html`
- Create: `tests/test_dashboard_content_editing.py`

**Step 1: Write the failing test**

```python
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from content.models import Page, PageSection


class DashboardContentEditingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="staff", password="pass12345", is_staff=True
        )
        self.page = Page.objects.create(slug="about", title="About", is_published=True)
        self.section = PageSection.objects.create(
            page=self.page, section_key="intro", heading="Old", body="Old body", display_order=1
        )
        self.client.force_login(self.user)

    def test_staff_can_update_section_text(self):
        url = reverse("dashboard:section_edit", args=[self.section.id])
        response = self.client.post(url, {"heading": "New", "body": "<p>Updated</p>", "display_order": 1, "is_active": True})
        self.assertEqual(response.status_code, 302)
        self.section.refresh_from_db()
        self.assertEqual(self.section.heading, "New")
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_dashboard_content_editing.py -v 2`  
Expected: FAIL because edit form/view/route does not exist.

**Step 3: Write minimal implementation**

`dashboard/forms.py`:

```python
from django import forms
from content.models import PageSection, GalleryImage


class PageSectionForm(forms.ModelForm):
    class Meta:
        model = PageSection
        fields = ["heading", "body", "image", "display_order", "is_active"]


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["title", "caption", "category", "image", "display_order", "is_active"]
```

`dashboard/views.py` add CRUD views for:
- page list
- section edit
- gallery list
- gallery create/edit

On save:

```python
obj.updated_by = request.user
obj.save()
```

`dashboard/urls.py` add:

```python
path("pages/", views.page_list, name="page_list"),
path("sections/<int:pk>/edit/", views.section_edit, name="section_edit"),
path("gallery/", views.gallery_list, name="gallery_list"),
path("gallery/new/", views.gallery_create, name="gallery_create"),
path("gallery/<int:pk>/edit/", views.gallery_edit, name="gallery_edit"),
```

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_dashboard_content_editing.py -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add dashboard templates/dashboard tests/test_dashboard_content_editing.py
git commit -m "feat: implement dashboard content editing for sections and gallery images"
```

### Task 7: Rich Text and Upload Validation

**Files:**
- Modify: `dashboard/forms.py`
- Create: `tests/test_form_validation.py`

**Step 1: Write the failing test**

```python
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from dashboard.forms import GalleryImageForm


class GalleryImageFormValidationTests(SimpleTestCase):
    def test_rejects_non_image_file(self):
        bad_file = SimpleUploadedFile("bad.txt", b"not an image", content_type="text/plain")
        form = GalleryImageForm(data={"title": "Bad", "display_order": 1, "is_active": True}, files={"image": bad_file})
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_form_validation.py -v 2`  
Expected: FAIL because form currently accepts insufficiently validated input.

**Step 3: Write minimal implementation**

In `dashboard/forms.py`, add explicit image validation:

```python
def clean_image(self):
    image = self.cleaned_data.get("image")
    if not image:
        return image
    if image.size > 5 * 1024 * 1024:
        raise forms.ValidationError("Image must be 5MB or smaller.")
    return image
```

Also rely on `ImageField` and Pillow for type validation.

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_form_validation.py -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add dashboard/forms.py tests/test_form_validation.py
git commit -m "feat: enforce dashboard image upload validation"
```

### Task 8: Seed Initial Content and Final Verification

**Files:**
- Create: `content/management/__init__.py`
- Create: `content/management/commands/__init__.py`
- Create: `content/management/commands/seed_initial_content.py`
- Create: `tests/test_seed_command.py`
- Modify: `README.md`

**Step 1: Write the failing test**

```python
from django.core.management import call_command
from django.test import TestCase
from content.models import Page


class SeedCommandTests(TestCase):
    def test_seed_creates_required_pages(self):
        call_command("seed_initial_content")
        for slug in ["home", "about", "contact", "courses", "activities"]:
            self.assertTrue(Page.objects.filter(slug=slug).exists())
```

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests/test_seed_command.py -v 2`  
Expected: FAIL because command is missing.

**Step 3: Write minimal implementation**

Create command to `get_or_create` default pages and base sections.

```python
required_pages = ["home", "about", "contact", "courses", "activities"]
for slug in required_pages:
    Page.objects.get_or_create(slug=slug, defaults={"title": slug.title(), "is_published": True})
```

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests/test_seed_command.py -v 2`  
Expected: PASS.

**Step 5: Run full test suite**

Run: `python manage.py test -v 2`  
Expected: PASS for all tests.

**Step 6: Commit**

```bash
git add content/management tests/test_seed_command.py README.md
git commit -m "chore: add initial content seeding and project usage docs"
```

### Task 9: Manual Smoke Test Checklist

**Files:**
- Modify: `README.md`

**Step 1: Start dev server**

Run: `python manage.py runserver`

**Step 2: Verify public routes**

Check:
- `/`
- `/about/`
- `/contact/`
- `/courses/`
- `/activities/`
- `/gallery/`

Expected: pages render without server errors.

**Step 3: Verify admin layers**

Check:
- `/admin/` accessible to superuser.
- `/<SECRET_DASHBOARD_PATH>` accessible to staff/superuser.
- non-staff gets denied on hidden dashboard.

**Step 4: Verify edit/update flow**

In hidden dashboard:
- update rich text section content
- upload/replace image
- reorder display order

Expected: public pages immediately reflect updates.

**Step 5: Commit docs updates**

```bash
git add README.md
git commit -m "docs: add smoke test checklist for dashboard and public pages"
```
