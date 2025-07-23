from django.core.management.base import BaseCommand
from sales.models import OrderLine, OrderStats
from datetime import datetime, UTC, time
from dateutil.relativedelta import relativedelta
from sales.static.stats_schema_home import home_stats
from sales.static.stats_schema_items import items_stats
from django.conf import settings
from sales.services.calc_functions import calc_home_stats, calc_items_stats, convert_to_serializable
import copy

class Command(BaseCommand):
    help = "Computes and stores precomputed stats for the frontend | Clarity prioritzed over efficiency as this script will run overnight automatically"
    
    def handle(self, *args, **options):
        # Time based constants and variables
        today = datetime.now(UTC).date()
        item_name = 'Cinnamon' 
        
        # Delete old data to have a clean slate
        OrderStats.objects.all().delete()
        
        # Initializes dictionaries from stats schema
        both_home_stats = copy.deepcopy(home_stats)
        bakery_home_stats = copy.deepcopy(home_stats)
        cafe_home_stats = copy.deepcopy(home_stats)
        both_items_stats = copy.deepcopy(items_stats)
        bakery_items_stats = copy.deepcopy(items_stats)
        cafe_items_stats = copy.deepcopy(items_stats)
        
        # Perform calculations for all stats
        calc_home_stats(both_home_stats, OrderLine.objects.all().order_by('-date'))
        calc_home_stats(bakery_home_stats, OrderLine.objects.filter(location=settings.CONFIG['BAKERY_ID']).order_by('-date'))
        calc_home_stats(cafe_home_stats, OrderLine.objects.filter(location=settings.CONFIG['CAFE_ID']).order_by('-date'))
        calc_items_stats(both_items_stats, OrderLine.objects.filter(date__gte=today - relativedelta(days=90), name__icontains=item_name).order_by('-date'))
        calc_items_stats(bakery_items_stats, OrderLine.objects.filter(location=settings.CONFIG['BAKERY_ID'], date__gte=today - relativedelta(days=90), name__icontains=item_name).order_by('-date'))
        calc_items_stats(cafe_items_stats, OrderLine.objects.filter(location=settings.CONFIG['CAFE_ID'], date__gte=today - relativedelta(days=90), name__icontains=item_name).order_by('-date'))
        
        # Converts to serializable format
        both_home_stats = convert_to_serializable(both_home_stats)
        bakery_home_stats = convert_to_serializable(bakery_home_stats) 
        cafe_home_stats = convert_to_serializable(cafe_home_stats)
        both_items_stats = convert_to_serializable(both_items_stats)
        bakery_items_stats = convert_to_serializable(bakery_items_stats)
        cafe_items_stats = convert_to_serializable(cafe_items_stats)
        
        # Save the stats to the database model
        
        # HOME PAGE STATS
        OrderStats.objects.update_or_create(
            location='Both',
            defaults={'stats_json': both_home_stats}
        )
        OrderStats.objects.update_or_create(
            location='Bakery',
            defaults={'stats_json': bakery_home_stats}
        )
        OrderStats.objects.update_or_create(
            location='Cafe',
            defaults={'stats_json': cafe_home_stats}
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully computed and stored precomputed stats for the home page.'))
        
        # ITEMS PAGE STATS
        OrderStats.objects.update_or_create(
            location=f'Both_items_{item_name}',
            defaults={'stats_json': both_items_stats}
        )
        OrderStats.objects.update_or_create(
            location=f'Bakery_items_{item_name}',
            defaults={'stats_json': bakery_items_stats}
        )
        OrderStats.objects.update_or_create(
            location=f'Cafe_items_{item_name}',
            defaults={'stats_json': cafe_items_stats}
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully computed and stored precomputed stats for the items page.'))
        
        