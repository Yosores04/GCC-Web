from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site_settings(request):
    try:
        settings_obj = SiteSettings.load()
    except (OperationalError, ProgrammingError):
        settings_obj = None
    return {"site_settings": settings_obj}
