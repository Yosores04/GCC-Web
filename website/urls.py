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
