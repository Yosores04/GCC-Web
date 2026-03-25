from django.core.management.base import BaseCommand, CommandError

from content.client_packaging import apply_import_payload, read_payload_from_file


class Command(BaseCommand):
    help = "Import site settings, pages, sections, and gallery data from a JSON client package."

    def add_arguments(self, parser):
        parser.add_argument("input_path", help="Source JSON filepath.")
        parser.add_argument(
            "--merge",
            action="store_true",
            help="Merge with existing records instead of resetting content first.",
        )

    def handle(self, *args, **options):
        try:
            payload = read_payload_from_file(options["input_path"])
        except FileNotFoundError as exc:
            raise CommandError(f"Input file not found: {options['input_path']}") from exc
        except ValueError as exc:
            raise CommandError("Invalid JSON content.") from exc

        summary = apply_import_payload(payload, reset_existing=not options["merge"])
        self.stdout.write(
            self.style.SUCCESS(
                "Import complete. "
                f"Pages: {summary['pages_written']}, "
                f"Sections: {summary['sections_written']}, "
                f"Gallery: {summary['gallery_written']}."
            )
        )
