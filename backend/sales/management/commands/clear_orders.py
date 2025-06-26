from django.core.management.base import BaseCommand
from sales.models import OrderLine

class Command(BaseCommand):
    help = 'Clears all OrderLine data from the database'
    
    def handle(self, *args, **options):
        count = OrderLine.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} order lines.'))