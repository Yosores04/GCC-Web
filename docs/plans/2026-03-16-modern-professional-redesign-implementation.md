# Modern Professional Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refresh the public GCC website UI into a modern, professional design with self-hosted typography and improved responsive layout.

**Architecture:** Move presentation concerns from inline template CSS into a centralized static stylesheet, apply new semantic layout classes across public templates, and add self-hosted font assets loaded through `@font-face`. Keep backend logic and dashboard behavior unchanged.

**Tech Stack:** Django templates, Django staticfiles, CSS (custom properties, responsive layout, lightweight motion), existing Django test suite.

---

### Task 1: Add redesign regression test (TDD)

**Files:**
- Modify: `tests/test_public_pages.py`
- Test: `tests/test_public_pages.py`

**Step 1: Write the failing test**

Add a test that asserts the new markup primitives exist:
- `class="site-header"`
- `class="top-nav"`
- `class="content-card"`

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests.test_public_pages.PublicPageTests.test_home_page_uses_modern_layout_markup -v 2`  
Expected: FAIL because new classes are not in the old template.

**Step 3: Write minimal implementation**

Update templates to include the expected structure/classes.

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests.test_public_pages.PublicPageTests.test_home_page_uses_modern_layout_markup -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/test_public_pages.py templates/base.html templates/website/home.html templates/website/page.html templates/website/gallery.html
git commit -m "test: add layout markup coverage for modern public templates"
```

### Task 2: Create centralized modern stylesheet + font loading

**Files:**
- Create: `static/css/site.css`
- Modify: `templates/base.html`

**Step 1: Write the failing test**

Extend test to assert stylesheet link exists:
- `/static/css/site.css`

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests.test_public_pages.PublicPageTests.test_home_page_uses_modern_layout_markup -v 2`  
Expected: FAIL because stylesheet link is missing.

**Step 3: Write minimal implementation**

- Add `{% load static %}` in `base.html`
- Reference `static/css/site.css`
- Move inline CSS into external stylesheet
- Define design tokens, typography, nav, cards, responsive behavior, and motion

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests.test_public_pages.PublicPageTests.test_home_page_uses_modern_layout_markup -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add static/css/site.css templates/base.html tests/test_public_pages.py
git commit -m "feat: add centralized modern styling system for public site"
```

### Task 3: Add self-hosted font assets and wire @font-face

**Files:**
- Create: `static/fonts/Manrope-VariableFont_wght.ttf`
- Create: `static/fonts/SpaceGrotesk-VariableFont_wght.ttf`
- Modify: `static/css/site.css`

**Step 1: Write the failing test**

Add assertions in test for font family declarations in response-visible markup context (e.g., body class or style hook) if needed.

**Step 2: Run test to verify it fails**

Run: `python manage.py test tests.test_public_pages.PublicPageTests.test_home_page_uses_modern_layout_markup -v 2`  
Expected: FAIL before font hooks exist.

**Step 3: Write minimal implementation**

Define `@font-face` blocks in `site.css` with:
- `font-family: "Manrope";`
- `font-family: "Space Grotesk";`
- `font-display: swap;`

Assign:
- Body/UI -> Manrope
- Heading/nav -> Space Grotesk

**Step 4: Run test to verify it passes**

Run: `python manage.py test tests.test_public_pages.PublicPageTests.test_home_page_uses_modern_layout_markup -v 2`  
Expected: PASS.

**Step 5: Commit**

```bash
git add static/fonts static/css/site.css tests/test_public_pages.py
git commit -m "feat: add self-hosted typography for modern redesign"
```

### Task 4: Final verification and docs update

**Files:**
- Modify: `README.md`

**Step 1: Run focused tests**

Run:
- `python manage.py test tests.test_public_pages -v 2`

Expected: PASS.

**Step 2: Run full test suite**

Run:
- `python manage.py test tests -v 2`

Expected: PASS.

**Step 3: Update docs**

Add short section to README noting:
- public style system location `static/css/site.css`
- font assets location `static/fonts/`

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: document redesign styling and typography assets"
```
