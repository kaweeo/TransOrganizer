from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from common.services.fuel_prices import update_croatia_prices


class Command(BaseCommand):
    help = "Fetch and cache Croatia fuel prices from CollectAPI."

    def handle(self, *args, **options):
        if not settings.COLLECTAPI_API_KEY:
            raise CommandError("COLLECTAPI_API_KEY is not set")

        updated = update_croatia_prices()
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} fuel price entries."))
