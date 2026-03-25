# Gingoog City Colleges Website (Django)

This project includes:

- Public website pages (`/`, `/about/`, `/contact/`, `/courses/`, `/activities/`, `/gallery/`)
- Hidden content dashboard for staff/superusers (`/<SECRET_DASHBOARD_PATH>`)
- Standard Django admin (`/admin/`)
- Rich text and image management for content updates

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create environment file:

```bash
copy .env.example .env
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Seed default pages:

```bash
python manage.py seed_initial_content
```

6. Start the server:

```bash
python manage.py runserver
```

## Sellable Single-School Workflow

This project is intentionally single-site per deployment (one `SiteSettings` record), which is ideal for reusing the same codebase for different school clients one at a time.

### Extended Site Settings (Admin)

In `/admin/`, `Site Settings` now supports:

- Branding: `school_name`, `tagline`, `logo`
- Contact: `contact_email`, `contact_phone`, `address`, `map_embed_url`
- Links: `website_url`, `admissions_url`, `facebook_url`, `instagram_url`, `youtube_url`

### One-Click New Client Onboarding

Reset content and reseed the full page blueprint:

```bash
python manage.py onboard_new_client --school-name "Sample Academy" --tagline "Future-ready learning"
```

Optional fields:

```bash
python manage.py onboard_new_client \
  --school-name "Sample Academy" \
  --tagline "Future-ready learning" \
  --contact-email "info@sample.edu" \
  --contact-phone "+63 999 000 0000" \
  --address "Sample City" \
  --website-url "https://sample.edu" \
  --admissions-url "https://sample.edu/admissions" \
  --facebook-url "https://facebook.com/sample" \
  --instagram-url "https://instagram.com/sample" \
  --youtube-url "https://youtube.com/sample"
```

### Export Client Package

```bash
python manage.py export_site_content client-a.json
```

Exports:

- Site settings
- Pages and sections
- Gallery metadata

### Import Client Package

```bash
python manage.py import_site_content client-a.json
```

Use merge mode if you need additive import:

```bash
python manage.py import_site_content client-a.json --merge
```

## Hidden Dashboard

- URL path comes from `.env` key: `SECRET_DASHBOARD_PATH`
- Example:

```env
SECRET_DASHBOARD_PATH=control-room-2026/
```

- Full URL in development:
  - `http://127.0.0.1:8000/control-room-2026/`

## Running Tests

Run all current tests in the top-level test package:

```bash
python manage.py test tests -v 2
```

## Switch to MySQL (with existing SQLite data)

1. Keep `DB_ENGINE=sqlite` first (or remove `DB_ENGINE`) and export current data:

```bash
python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --indent 2 > data_migration.json
```

2. Set MySQL environment values in `.env`:

```env
DB_ENGINE=mysql
DB_NAME=gcc_site
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

3. Make sure MySQL server is running and the database exists, then run:

```bash
python manage.py migrate
python manage.py loaddata data_migration.json
```

4. Verify:

```bash
python manage.py check
python manage.py runserver
```

## Notes

- Images are stored locally in `media/` for now.
- A future cloud migration (S3/Cloudinary) can be added by swapping Django storage settings.
- Public redesign styles live in `static/css/site.css`.
- Self-hosted typography assets live in `static/fonts/`.
- Public carousel behavior lives in `static/js/site.js`.
- Run `python manage.py seed_initial_content` anytime to re-ensure the mapped page section blueprint and placeholders.
