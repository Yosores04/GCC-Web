from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from content.models import GalleryImage, Page, PageSection

from .forms import GalleryImageForm, PageSectionForm

def _ensure_editor(user):
    if user.is_staff or user.is_superuser:
        return
    raise PermissionDenied("Staff access required.")


@login_required
def index(request):
    _ensure_editor(request.user)
    return render(request, "dashboard/index.html")


@login_required
def page_list(request):
    _ensure_editor(request.user)
    pages = Page.objects.all().order_by("title", "id")
    return render(request, "dashboard/page_list.html", {"pages": pages})


@login_required
def section_edit(request, pk):
    _ensure_editor(request.user)
    section = get_object_or_404(PageSection, pk=pk)

    if request.method == "POST":
        form = PageSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_by = request.user
            updated.save()
            return redirect("dashboard:page_list")
    else:
        form = PageSectionForm(instance=section)

    return render(
        request,
        "dashboard/section_form.html",
        {"form": form, "section": section},
    )


@login_required
def gallery_list(request):
    _ensure_editor(request.user)
    items = GalleryImage.objects.all().order_by("display_order", "id")
    return render(request, "dashboard/gallery_list.html", {"items": items})


@login_required
def gallery_create(request):
    _ensure_editor(request.user)
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES, allow_multiple_upload=True)
        uploaded_images = request.FILES.getlist("image")

        if not uploaded_images:
            form.add_error("image", "Please upload at least one image.")

        if form.is_valid():
            oversized = [img.name for img in uploaded_images if img.size > 5 * 1024 * 1024]
            if oversized:
                form.add_error("image", "Image must be 5MB or smaller.")
            else:
                title = form.cleaned_data["title"]
                caption = form.cleaned_data["caption"]
                category = form.cleaned_data["category"]
                display_order = form.cleaned_data["display_order"]
                is_active = form.cleaned_data["is_active"]

                for index, image in enumerate(uploaded_images):
                    item_title = title if index == 0 else f"{title} ({index + 1})"
                    GalleryImage.objects.create(
                        title=item_title,
                        caption=caption,
                        category=category,
                        image=image,
                        display_order=display_order + index,
                        is_active=is_active,
                        updated_by=request.user,
                    )
                return redirect("dashboard:gallery_list")
    else:
        form = GalleryImageForm(allow_multiple_upload=True)

    return render(
        request,
        "dashboard/gallery_form.html",
        {"form": form, "is_create": True},
    )


@login_required
def gallery_edit(request, pk):
    _ensure_editor(request.user)
    item = get_object_or_404(GalleryImage, pk=pk)

    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_by = request.user
            updated.save()
            return redirect("dashboard:gallery_list")
    else:
        form = GalleryImageForm(instance=item)

    return render(
        request,
        "dashboard/gallery_form.html",
        {"form": form, "item": item, "is_create": False},
    )
