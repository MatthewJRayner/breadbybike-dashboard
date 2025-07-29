from django.core.management.base import BaseCommand
from sales.models import DailyOrderSnapshot, OrderStats, OrderLine
from sales.services.fetch_orders_today import fetch_orders_today
from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta
from sales.services.calc_functions import convert_to_serializable, calc_daily_stats_home, calc_daily_stats_items, convert_from_serializable
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
        today_orders = fetch_orders_today()
        if len(today_orders) > 2:
            # Reset the DailyOrderSnapshot model
            DailyOrderSnapshot.objects.filter(date=today).delete()
            
            # Fetch stats from models
            both_stats_dict = convert_from_serializable(OrderStats.objects.get(location='Both').stats_json)
            bakery_stats_dict = convert_from_serializable(OrderStats.objects.get(location='Bakery').stats_json)
            cafe_stats_dict = convert_from_serializable(OrderStats.objects.get(location='Cafe').stats_json)
            both_items_dict = convert_from_serializable(OrderStats.objects.get(location=f'Both_items_{item_name}').stats_json)
            bakery_items_dict = convert_from_serializable(OrderStats.objects.get(location=f'Bakery_items_{item_name}').stats_json)
            cafe_items_dict = convert_from_serializable(OrderStats.objects.get(location=f'Cafe_items_{item_name}').stats_json)
            
            # Set model data back to zero
            OrderStats.objects.filter(location='Both').update(stats_json=convert_to_serializable(copy.deepcopy(home_stats)))
            OrderStats.objects.filter(location='Both').update(stats_json=convert_to_serializable(copy.deepcopy(home_stats)))
            OrderStats.objects.filter(location='Both').update(stats_json=convert_to_serializable(copy.deepcopy(home_stats)))
            OrderStats.objects.filter(location=f'Both_items_{item_name}').update(stats_json=convert_to_serializable(copy.deepcopy(items_stats)))
            OrderStats.objects.filter(location=f'Both_items_{item_name}').update(stats_json=convert_to_serializable(copy.deepcopy(items_stats)))
            OrderStats.objects.filter(location=f'Both_items_{item_name}').update(stats_json=convert_to_serializable(copy.deepcopy(items_stats)))
            
            both_stats_dict['daily_home_stats'] = copy.deepcopy(home_stats['daily_home_stats'])
            bakery_stats_dict['daily_home_stats'] = copy.deepcopy(home_stats['daily_home_stats'])
            cafe_stats_dict['daily_home_stats'] = copy.deepcopy(home_stats['daily_home_stats'])
            both_items_dict['daily_items_stats'] = copy.deepcopy(items_stats['daily_items_stats'])
            bakery_items_dict['daily_items_stats'] = copy.deepcopy(items_stats['daily_items_stats'])
            cafe_items_dict['daily_items_stats'] = copy.deepcopy(items_stats['daily_items_stats'])
            
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
            calc_daily_stats_home(both_stats_dict, DailyOrderSnapshot.objects.all())
            calc_daily_stats_home(bakery_stats_dict, DailyOrderSnapshot.objects.filter(location=settings.CONFIG['BAKERY_ID']))
            calc_daily_stats_home(cafe_stats_dict, DailyOrderSnapshot.objects.filter(location=settings.CONFIG['CAFE_ID']))
            calc_daily_stats_items(both_items_dict, DailyOrderSnapshot.objects.filter(name__icontains=item_name))
            calc_daily_stats_items(bakery_items_dict, DailyOrderSnapshot.objects.filter(name__icontains=item_name, location=settings.CONFIG['BAKERY_ID']))
            calc_daily_stats_items(cafe_items_dict, DailyOrderSnapshot.objects.filter(name__icontains=item_name, location=settings.CONFIG['CAFE_ID']))
            
            # Upload the stats to the OrderStats model
            OrderStats.objects.update_or_create(
                location=f'Both',
                defaults={'stats_json': convert_to_serializable(both_stats_dict)}
            )
            OrderStats.objects.update_or_create(
                location=f'Bakery',
                defaults={'stats_json': convert_to_serializable(bakery_stats_dict)}
            )
            OrderStats.objects.update_or_create(
                location=f'Cafe',
                defaults={'stats_json': convert_to_serializable(cafe_stats_dict)}
            )
            OrderStats.objects.update_or_create(
                location=f'Both_items_{item_name}',
                defaults={'stats_json': convert_to_serializable(both_items_dict)}
            )
            OrderStats.objects.update_or_create(
                location=f'Bakery_items_{item_name}',
                defaults={'stats_json': convert_to_serializable(bakery_items_dict)}
            )
            OrderStats.objects.update_or_create(
                location=f'Cafe_items_{item_name}',
                defaults={'stats_json': convert_to_serializable(cafe_items_dict)}
            )
            
            self.stdout.write(self.style.SUCCESS('Successfully computed and stored precomputed stats for the home and items pages.'))
        else:
            self.stdout.write(self.style.SUCCESS('Not enough orders to update so current stats kept.'))