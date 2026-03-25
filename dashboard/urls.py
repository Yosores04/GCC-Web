from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("pages/", views.page_list, name="page_list"),
    path("sections/<int:pk>/edit/", views.section_edit, name="section_edit"),
    path("gallery/", views.gallery_list, name="gallery_list"),
    path("gallery/new/", views.gallery_create, name="gallery_create"),
    path("gallery/<int:pk>/edit/", views.gallery_edit, name="gallery_edit"),
]
