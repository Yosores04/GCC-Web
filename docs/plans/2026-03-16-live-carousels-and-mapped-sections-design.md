# Live Carousels and Mapped Sections Design

**Date:** 2026-03-16  
**Project:** Gingoog City Colleges Website

## Objective

Upgrade the public website into a professional school-style experience by:

- adding live carousels on key pages
- pre-mapping page sections so structure is always polished
- limiting editor work to text/image updates in the dashboard

## Approved Direction

- Carousel scope:
  - Home hero
  - Activities highlights
  - Gallery hero/preview
- Section mapping:
  - fixed blueprint per page
  - placeholders pre-seeded (text + images)
  - dashboard edits content, not layout

## Section Blueprint

- `home`: `hero-carousel`, `welcome-intro`, `program-highlights`, `news-strip`, `cta-band`
- `about`: `hero-banner`, `institution-story`, `mission-vision`, `leadership-preview`, `cta-band`
- `courses`: `hero-banner`, `program-overview`, `course-grid`, `admissions-cta`, `faq-teaser`
- `activities`: `hero-banner`, `activities-carousel`, `student-life-grid`, `events-teaser`, `cta-band`
- `contact`: `hero-banner`, `contact-details`, `map-block`, `inquiry-cta`, `social-links`
- `gallery`: `hero-banner`, `gallery-carousel`, `album-grid`, `campus-life-text`, `cta-band`

## UX and Presentation

- Keep existing modern public typography and palette.
- Add a reusable carousel component with:
  - autoplay
  - previous/next controls
  - dot pagination
  - pause-on-hover/focus
  - reduced-motion support
- Keep dashboard architecture unchanged; content remains editable there.

## Data and Seeding

- Expand seeding to ensure all mapped keys exist for each page.
- Preserve idempotency and avoid duplicate sections on reruns.
- Ensure placeholder image assignment for missing images.
- Include gallery page in required page seed list.

## Verification

- Add/adjust tests for:
  - mapped section key generation
  - idempotent section count
  - carousel markup presence on target pages
- Run full test suite before completion.
