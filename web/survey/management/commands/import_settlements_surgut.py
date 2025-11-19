import csv
from django.core.management.base import BaseCommand
from survey.models import Settlement

class Command(BaseCommand):
    help = "Import settlements for Surgutsky rayon"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Path to CSV file with settlements"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        if not file_path:
            self.stderr.write("Error: --file argument required")
            return

        with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            created = 0
            updated = 0
            for row in reader:
                name = row["name"].strip()
                type_ = row["type"].strip()
                priority = int(row.get("priority", 999))

                obj, was_created = Settlement.objects.update_or_create(
                    name=name,
                    defaults={
                        "type": type_,
                        "priority": priority,
                    }
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

            self.stdout.write(self.style.SUCCESS(
                f"Import completed: created={created}, updated={updated}"
            ))
