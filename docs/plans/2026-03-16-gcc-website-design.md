# GCC Website Design

**Date:** 2026-03-16  
**Project:** Gingoog City Colleges Website

## Goals

- Build a Django website with public pages: `home`, `about`, `contact`, `courses`, `activities`, and `gallery`.
- Provide a hidden custom dashboard for content editing.
- Keep Django `/admin/` available for full administrative control.
- Allow staff/superusers to update text and images without touching code.

## Confirmed Decisions

- Site structure: Hybrid (separate page routes with reusable sections).
- Dashboard access: both hidden custom dashboard and Django admin.
- Content editing: rich text editor for section content.
- Image storage: local storage first, architecture ready for future cloud migration.
- Dashboard permissions: `is_staff` or `is_superuser`.

## Architecture

- Django project with apps:
  - `website` (public views/templates)
  - `content` (CMS models and forms)
  - `dashboard` (hidden staff editor UI)
- Public routes:
  - `/`
  - `/about/`
  - `/contact/`
  - `/courses/`
  - `/activities/`
  - `/gallery/`
- Hidden dashboard route:
  - Derived from environment variable `SECRET_DASHBOARD_PATH`.
  - Example value: `control-room-2026/`.

## Content Model

- `SiteSettings` (singleton):
  - School name, logo, email, phone, address, social links.
- `Page`:
  - `slug`, `title`, `meta_title`, `meta_description`, `is_published`.
- `PageSection`:
  - Foreign key to `Page`
  - `section_key`, `heading`, `body` (rich text), optional `image`
  - `display_order`, `is_active`
  - Audit fields `updated_at`, `updated_by`
- `GalleryImage`:
  - `title`, `caption`, `image`, `category`, `display_order`, `is_active`
  - Audit fields `updated_at`, `updated_by`

## Dashboard Behavior and Security

- Authentication required.
- Authorization: staff or superuser only.
- Non-authorized users: redirect to login or return HTTP 403.
- Dashboard capabilities:
  - Edit page sections (rich text + image).
  - Upload/update gallery images.
  - Reorder sections and gallery items.
  - Toggle publish/active state.
  - Quick links to preview public pages.

## Data Flow

1. Staff logs in and navigates to hidden dashboard path.
2. Staff edits `PageSection` and `GalleryImage` records.
3. Public views render only active/published content.
4. Templates output sections ordered by `display_order`.

## Error Handling

- Unknown page slug: HTTP 404.
- Missing optional section/image: hide block, no server error.
- Invalid upload type/size: display form errors.
- Permission failures: HTTP 403 or login redirect.

## Testing Strategy

- Model tests:
  - ordering, publish/active toggles, singleton settings behavior.
- Permission tests:
  - anonymous blocked, non-staff blocked, staff/superuser allowed.
- View tests:
  - all public pages and hidden dashboard routes.
- Form tests:
  - rich text fields and image validation.
- Smoke tests:
  - media serving in development.

## Implementation Constraints

- Follow TDD for implementation tasks.
- Keep UI and model design DRY and YAGNI.
- Keep `/admin/` and hidden dashboard separate by purpose.
