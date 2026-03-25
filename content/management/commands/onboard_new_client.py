from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from content.models import GalleryImage, Page, PageSection, SiteSettings


class Command(BaseCommand):
    help = "Reset content to a fresh blueprint and apply starter site settings for a new client school."

    def add_arguments(self, parser):
        parser.add_argument("--school-name", default="Gingoog City Colleges")
        parser.add_argument("--tagline", default="")
        parser.add_argument("--contact-email", default="")
        parser.add_argument("--contact-phone", default="")
        parser.add_argument("--address", default="")
        parser.add_argument("--facebook-url", default="")
        parser.add_argument("--instagram-url", default="")
        parser.add_argument("--youtube-url", default="")
        parser.add_argument("--website-url", default="")
        parser.add_argument("--admissions-url", default="")
        parser.add_argument("--map-embed-url", default="")
        parser.add_argument(
            "--keep-gallery",
            action="store_true",
            help="Keep existing gallery records instead of clearing them.",
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            PageSection.objects.all().delete()
            Page.objects.all().delete()
            if not options["keep_gallery"]:
                GalleryImage.objects.all().delete()

            settings_obj = SiteSettings.load()
            settings_obj.school_name = options["school_name"].strip() or "Gingoog City Colleges"
            settings_obj.tagline = options["tagline"].strip()
            settings_obj.logo = None
            settings_obj.contact_email = options["contact_email"].strip()
            settings_obj.contact_phone = options["contact_phone"].strip()
            settings_obj.address = options["address"].strip()
            settings_obj.facebook_url = options["facebook_url"].strip()
            settings_obj.instagram_url = options["instagram_url"].strip()
            settings_obj.youtube_url = options["youtube_url"].strip()
            settings_obj.website_url = options["website_url"].strip()
            settings_obj.admissions_url = options["admissions_url"].strip()
            settings_obj.map_embed_url = options["map_embed_url"].strip()
            settings_obj.save()

        call_command("seed_initial_content")
        self.stdout.write(
            self.style.SUCCESS(
                "Onboarding complete. Content reset, blueprint seeded, and site settings updated."
            )
        )
