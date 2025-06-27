from django.core.management.base import BaseCommand
from sales.models import OrderLine
import json
from datetime import datetime, UTC
import calendar
from dateutil.relativedelta import relativedelta
from sales.static.stats_schema import both_stats, bakery_stats, cafe_stats
from config import CONFIG

class Command(BaseCommand):
    help = "Computes and stores precomputed stats for the frontend | Clarity prioritzed over efficiency as this script will run overnight automatically"
    
    def handle(self, *args, **options):
        start_date = (today - relativedelta(years=1, months=1)).replace(day=1)
        today = datetime.now(UTC).date()
        current_month = today.month
        current_year = today.year
        previous_month = today.month-1
        last_week_start = (today - relativedelta(days=7))
        last_week_end = (today - relativedelta(days=1))
        current_month = today.month
        
        both_stats_calc = both_stats
        bakery_stats_calc = bakery_stats
        cafe_stats_calc = cafe_stats # Will be used to calculated mainly growth percentage
        orders = OrderLine.objects.filter(date__gte=start_date)
        
        # Big for loop to add data incrementally and then check for location to add data to 
        for order in orders:
            if order.date.year == today.year:
                both_stats_calc['home_stats']['year_sales_graph']['total_sales_year']['total_sales_year'] += order.total_sale
                if order.date.year < current_year and order.date.month == current_month:
                    both_stats_calc['post_calc_stats']['previous_year_same_month_total'] += order.total_sale
                if order.date.month == current_month:
                    both_stats_calc['home_stats']['monthly_sales_graph']['total_sales_month'],
                    both_stats_calc['home_stats']['monthly_stats_tiles']['total_sales_month'] += order.total_sale
                    
                for i in range(1, current_month + 1):
                    if order.date.month == i:
                        both_stats_calc['home_stats']['year_sales_graph']['graphs'][f'month{i}'] += order.total_sale
                
            
            
            if order.location == CONFIG['BAKERY_ID']:
                print(4)
            elif order.location == CONFIG['CAFE_ID']:
                print(3)
        
        # Label Creation
        for i in range(current_month):
            both_stats_calc['home_stats']['year_sales_graph']['labels'].append(f"{current_month - relativedelta(months=i)} '25")
            bakery_stats_calc['home_stats']['year_sales_graph']['labels'].append(f"{current_month - relativedelta(months=i)} '25")
            cafe_stats_calc['home_stats']['year_sales_graph']['labels'].append(f"{current_month - relativedelta(months=i)} '25")
        both_stats_calc['home_stats']['year_sales_graph']['labels'].reverse()
        bakery_stats_calc['home_stats']['year_sales_graph']['labels'].reverse()
        cafe_stats_calc['home_stats']['year_sales_graph']['labels'].reverse()
        
        # Post for loop calculations
        both_stats_calc['home_stats']['year_sales_graph']['monthly_avarage'] = both_stats_calc['home_stats']['year_sales_graph']['total_sales_year'] / today.month