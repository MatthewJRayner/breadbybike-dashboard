from django.core.management.base import BaseCommand
from sales.models import DailyOrderSnapshot, OrderStats, OrderLine
from sales.services.fetch_orders_new import fetch_orders_new
from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta
from sales.services.calc_functions import calc_items_stats, convert_to_serializable, calc_daily_stats_home, calc_daily_stats_items, convert_from_serializable
from sales.static.stats_schema_items import items_stats
from sales.static.stats_schema_home import home_stats
from django.conf import settings
import json
import copy

class Command(BaseCommand):
    help = "Script to run on page load to fetch daily orders and update the OrderStats model used for the frontend."
    
    def handle(self, *args, **options):
        # CONSTANTS / VARIABLES
        item_name = 'Cinnamon' # Default item name, this will later be grabbed from frontend
        today = datetime.now(UTC).date()
        today_orders = fetch_orders_new()
        if len(today_orders) > 2:
            # Fetch stats from models
            stats_obj = OrderStats.objects.get(location='Both')
            stats_dict = convert_from_serializable(stats_obj.stats_json)
            stats_dict['daily_home_stats'] = copy.deepcopy(home_stats['daily_home_stats'])
            stats_obj.stats_json = stats_dict
            stats_obj.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched stats for all locations and {item_name}.'))
            
            for order in today_orders:
                if not order.line_items:
                    continue
                
                for item in order.line_items:
                    DailyOrderSnapshot.objects.create(
                        name=item.name or 'Custom',
                        quantity=int(item.quantity) if item.quantity else 1,
                        location=order.location_id,
                        date=today,
                        time=order.created_at[11:19],
                        total_sale=round(item.total_money.amount / 100, 2) if item.total_money.amount else 0,
                        discount=round(item.total_discount_money.amount / 100, 2) if item.total_discount_money.amount else 0,
                        service_charge=round((order.total_service_charge_money.amount // len(order.line_items)) / 100, 2) if order.total_service_charge_money.amount else 0,
                        tax=round(item.total_tax_money.amount / 100, 2) if item.total_tax_money.amount else 0,
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(today_orders)} new daily orders.'))   
            
            # Perform calculations on objects in DailyOrderSnapshot
            calc_daily_stats_home(stats_dict, DailyOrderSnapshot.objects.filter(location=settings.CONFIG['BAKERY_ID']))
            
            # Upload the stats to the OrderStats model
            stats_obj.stats_json = stats_dict
            stats_obj.save()
            
            self.stdout.write(self.style.SUCCESS('Successfully computed and stored precomputed stats for the home and items pages.'))
        else:
            self.stdout.write(self.style.SUCCESS('Not enough orders to update so current stats kept.'))