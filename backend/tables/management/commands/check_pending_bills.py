from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from tables.models import Table

class Command(BaseCommand):
    help = "Check tables with pending bills and notify cashier/manager"

    def handle(self, *args, **options):
        threshold_minutes = 15
        threshold_time = timezone.now() - timedelta(minutes=threshold_minutes)

        pending_tables = Table.objects.filter(
            status=Table.Status.BILL_REQUESTED,
            last_status_change__lte=threshold_time
        )

        if not pending_tables.exists():
            self.stdout.write("No pending bills found.")
            return

        for table in pending_tables:
            self.stdout.write(
                f"⚠️ ALERT: Table {table.number} pending bill for more than {threshold_minutes} minutes"
            )
