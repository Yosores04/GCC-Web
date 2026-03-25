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
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.updated_by = request.user
            item.save()
            return redirect("dashboard:gallery_list")
    else:
        form = GalleryImageForm()

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
