from django.core.management.base import BaseCommand

from content.client_packaging import build_export_payload, write_payload_to_file


class Command(BaseCommand):
    help = "Export site settings, pages, sections, and gallery data to a JSON client package."

    def add_arguments(self, parser):
        parser.add_argument(
            "output_path",
            nargs="?",
            default="client-content-export.json",
            help="Destination JSON filepath.",
        )

    def handle(self, *args, **options):
        payload = build_export_payload()
        destination = write_payload_to_file(payload, options["output_path"])
        self.stdout.write(
            self.style.SUCCESS(f"Export complete: {destination.resolve()}")
        )
