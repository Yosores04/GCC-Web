# Modern Professional Redesign Design

**Date:** 2026-03-16  
**Project:** Gingoog City Colleges Website

## Goal

Revise the public website visual design to feel modern and professional, with original typography and no copied font styling.

## Confirmed Decisions

- Visual blend: Clean Corporate + Bold Contemporary.
- Typography strategy: self-hosted fonts.
- Navigation style: clean modern nav, no slash separators.
- Brand direction: strong hierarchy, polished cards, subtle motion.

## Visual System

- Self-hosted font pair:
  - Headings/navigation: Space Grotesk
  - Body/interface text: Manrope
- Color direction:
  - light neutral page background
  - deep navy accent for professional tone
  - near-black text for readability
  - muted cool accent for interactive highlights
- Design rhythm:
  - large, confident headings
  - generous section spacing
  - consistent visual hierarchy

## Layout and Navigation

- Sticky top header with backdrop blur and subtle border.
- Simplified horizontal nav:
  - no slash separators
  - compact uppercase links
  - animated underline hover/active treatment
- Responsive behavior:
  - wrapped/stacked nav on smaller screens
  - reduced type scale and spacing for mobile

## Component Styling

- Public content sections render as clean cards with:
  - rounded corners
  - subtle borders and soft shadows
  - optional image styling with rounded media frames
- Rich text readability improvements:
  - paragraph spacing
  - list indentation/spacing
  - link emphasis and hover behavior

## Motion and Interaction

- Page-load reveal animation for core content.
- Hover lift effects on content cards.
- Smooth nav underline transitions.
- Keep motion subtle and professional.

## Accessibility and Performance

- Maintain semantic structure and alt text behavior.
- Preserve visible focus indicators for keyboard users.
- Use strong color contrast for text and interactive elements.
- Self-hosted fonts with `font-display: swap`.
- Keep redesign lightweight without heavy frontend frameworks.

## Affected Scope

- Public templates and styling only:
  - `templates/base.html`
  - `templates/website/home.html`
  - `templates/website/page.html`
  - `templates/website/gallery.html`
  - new static CSS and font assets under `static/`
- Dashboard/admin experience remains functionally unchanged.
