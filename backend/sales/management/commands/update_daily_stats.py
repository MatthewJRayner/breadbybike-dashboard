from django.core.management.base import BaseCommand
from sales.models import DailyOrderSnapshot, OrderStats, OrderLine
from sales.services.fetch_orders_new import fetch_orders_new
from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta
from sales.services.calc_functions import calc_items_stats, convert_to_serializable, calc_daily_stats_home, calc_daily_stats_items, convert_from_serializable
from sales.static.stats_schema_items import items_stats
import json
import copy

class Command(BaseCommand):
    help = "Script to run on page load to fetch daily orders and update the OrderStats model used for the frontend."
    
    def handle(self, *args, **options):
        # CONSTANTS / VARIABLES
        item_name = 'Wholemeal' # Example item name, this will later be grabbed from the frontend
        item_location = 'both' # Example location, this will later be grabbed from the frontend
        today = datetime.now(UTC).date()
        today_orders = fetch_orders_new()
        
        # Grab dictionaries for each page based on the item name and location
        stats_dicts = {}
        
        try:
            stats_dicts[f'{item_location}'] = convert_from_serializable(OrderStats.objects.get(location=f'{item_location}').stats_json)
        except OrderStats.DoesNotExist:
            stats_dicts[f'{item_location}'] = {}
        
        # Rerun the calculation script if chosen item doesn't exist  
        item_key = f'{item_location}_items_{item_name}' 
        try:
            stats_dicts[item_key] = convert_from_serializable(OrderStats.objects.get(location=item_key).stats_json)
        except OrderStats.DoesNotExist:
            location_stats = copy.deepcopy(items_stats)
            querylist = OrderLine.objects.filter(date__gte=today - relativedelta(days=90), name=item_name).order_by('-date')
            if item_location in ['bakery', 'cafe']:
                querylist = querylist.filter(location=CONFIG[f'{item_location.upper()}_ID'])
            calc_items_stats(location_stats, querylist)
            stats_dicts[item_key] = location_stats
            # Save to OrderStats model
            OrderStats.objects.update_or_create(
                location=item_key,
                defaults={'stats_json': convert_to_serializable(location_stats)}
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched stats for {item_location} and {item_key}.'))
        
        for order in today_orders:
            if not order.line_items:
                continue
            
            for item in order.line_items:
                DailyOrderSnapshot.objects.create(
                    name=item.name or 'Custom',
                    quantity=int(item.quantity) if item.quantity else 1,
                    location=order.location_id,
                    date=today,
                    time=order.created_at[11:16],
                    total_sale=round(item.total_money.amount / 100, 2) if item.total_money.amount else 0
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(today_orders)} new daily orders.'))   
        
        # Perform calculations on objects in DailyOrderSnapshot
        calc_daily_stats_home(stats_dicts[f'{item_location}'], DailyOrderSnapshot.objects.filter(date__in=[today, today - relativedelta(days=1)]))
        calc_daily_stats_items(stats_dicts[item_key], DailyOrderSnapshot.objects.all())
        
        # Upload the stats to the OrderStats model
        OrderStats.objects.update_or_create(
            location=f'{item_location}',
            defaults={'stats_json': convert_to_serializable(stats_dicts[f'{item_location}'])}
        )
        OrderStats.objects.update_or_create(
            location=item_key,
            defaults={'stats_json': convert_to_serializable(stats_dicts[item_key])}
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully computed and stored precomputed stats for the home and items pages.'))