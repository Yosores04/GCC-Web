# Live Carousels and Mapped Sections Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver a mapped, professional school website with live carousels and editable section/image content.

**Architecture:** Expand section seeding from generic numbered blocks to a fixed per-page blueprint, derive ordered mapped sections in views, and render a reusable carousel component using lightweight JS/CSS.

**Tech Stack:** Django templates/views/management commands, Pillow, custom CSS, vanilla JS, Django test runner.

---

### Task 1: TDD for mapped section blueprint + idempotency

**Files:**
- Modify: `tests/test_seed_command.py`
- Test: `tests/test_seed_command.py`

**Steps:**
1. Replace numbered section expectations with key blueprint assertions.
2. Include gallery page in required pages assertion.
3. Verify expected total sections (`6 pages * 5 keys = 30`) after reruns.
4. Run failing tests first.

### Task 2: Implement mapped seeding behavior

**Files:**
- Modify: `content/management/commands/seed_initial_content.py`

**Steps:**
1. Add page blueprint constant with ordered section keys + placeholder text.
2. Ensure required pages include gallery.
3. Ensure mapped sections exist in display order with placeholder image if missing.
4. Keep command idempotent and rerunnable.
5. Run seed tests to green.

### Task 3: TDD for live carousel markup on public pages

**Files:**
- Modify: `tests/test_public_pages.py`
- Test: `tests/test_public_pages.py`

**Steps:**
1. Add tests for carousel markup on home and activities pages.
2. Ensure tests fail before template/view changes.

### Task 4: Implement mapped page rendering + carousel data

**Files:**
- Modify: `website/views.py`
- Modify: `templates/website/home.html`
- Modify: `templates/website/page.html`
- Modify: `templates/website/gallery.html`
- Modify: `templates/base.html`
- Create: `static/js/site.js`
- Modify: `static/css/site.css`

**Steps:**
1. Build helper logic to return ordered mapped sections for a page.
2. Build carousel slide payloads from mapped sections / gallery items.
3. Render carousel component in target templates.
4. Add JS behavior (autoplay, controls, dots, pause-on-hover).
5. Add CSS for carousel and mapped layout blocks.
6. Re-run public page tests to green.

### Task 5: Verify end-to-end

**Files:**
- Modify: `README.md` (if needed for usage note)

**Steps:**
1. Run `python manage.py test tests -v 2`.
2. Run `python manage.py seed_initial_content` on local db.
3. Confirm pages now render with mapped sections and live carousels.
