from django.core.management.base import BaseCommand
from sales.models import OrderStats

class Command(BaseCommand):
    help = 'Clears all OrderLine data from the database'
    
    def handle(self, *args, **options):
        count = OrderStats.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} order lines.'))