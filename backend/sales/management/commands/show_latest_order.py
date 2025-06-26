from django.core.management.base import BaseCommand
from sales.models import OrderLine

class Command(BaseCommand):
    help = "Shows the most recent order line in the database"

    def handle(self, *args, **options):
        latest = OrderLine.objects.order_by('-date', '-time').first()
        if latest:
            self.stdout.write(self.style.SUCCESS(f"Latest order:"))
            self.stdout.write(f"Name: {latest.name}")
            self.stdout.write(f"Date: {latest.date}")
            self.stdout.write(f"Time: {latest.time}")
            self.stdout.write(f"Location: {latest.location}")
            self.stdout.write(f"Quantity: {latest.quantity}")
            self.stdout.write(f"Total Sale: £{latest.total_sale:.2f}")
        else:
            self.stdout.write(self.style.WARNING("No order lines found."))