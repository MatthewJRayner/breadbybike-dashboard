from django.core.management.base import BaseCommand
from sales.models import OrderLine
import json
from datetime import datetime, UTC, timedelta, time
import calendar
import copy
from dateutil.relativedelta import relativedelta
from sales.static.stats_schema_items import stats
from config import CONFIG

class Command(BaseCommand):
    help = "Computes and stores precomputed stats for the frontend | Clarity prioritized over efficiency as this script will run overnight automatically"
    
    def handle(self, *args, **options):
        item_name = 'Cinnamon'
        # Time based constants and variables
        today = datetime.now(UTC).date()
        current_month = today.month
        current_year = today.year
        last_year_end = today - relativedelta(years=1, days=1)
        current_month = today.month
        start_time = time(hour=8, minute=0, second=0)  # Start of the day for sales calculations
        # Initializes dictionaries from stats schema
        both_items_stats = {k: v.copy() for k, v in stats.items()}
        bakery_items_stats = {k: v.copy() for k, v in stats.items()}
        cafe_items_stats = {k: v.copy() for k, v in stats.items()}
        helper = {
            'weekly_sales': {
                'previous_week': 0.00
            },
            'monthly_sales': {
                'previous_month': 0.00
            },
            'total_sales_last_week': {
                'count': 0
            },
            'daily_average': {
                'count_list': [0] * 7,
                'previous_week_count': [0] * 7,
                'previous_month_count': [0] * 30,    
            }
        }
        
        # FUNCTIONS
        def percent_increase(a, b):
            """ Returns the percent increase of two numbers, with a being the end variable and b being the original variable """
            return 0.00 if b == 0 else round(((a - b) / b) * 100, 2)
        
        
        def average(a):
            """ Returns the average of a list of numbers """
            return sum(a) / len(a) if a else 0.00
        
        
        def calc_items_stats(dictionary, querylist):
            """ Calculates the items stats for a given dictionary and querylist, assuming the querylist is filted to be the last 90 days """
            # Big for loop to iterate through all the items in the querylist
            for order in querylist:
                days_ago = (today - order.date).days
                time_block_index = ((order.time.hour - start_time.hour) * 60 - order.time.minute) // 30
            
                dictionary['last_3_months']['daily_graph']['graph'][days_ago-1] += order.quantity
                dictionary['last_3_months']['weekday_count_graph']['graph'][order.date.weekday()] += order.quantity
                if time_block_index < 16:
                    dictionary['last_3_months']['time_of_day_graph']['graph'][time_block_index] += order.quantity
                
                # ORDERS FROM LAST 30 DAYS
                if 1 <= days_ago <= 30:
                    dictionary['monthly_sales']['sales'] += order.total_sale
                    dictionary['last_month']['daily_graph']['graph'][days_ago-1] += order.quantity
                    dictionary['last_month']['weekday_count_graph']['graph'][order.date.weekday()] += order.quantity
                    helper['monthly_sales']['previous_month'] += order.total_sale
                    helper['daily_average']['previous_month_count'][days_ago-1] += order.quantity
                    if time_block_index < 16 and time_block_index >= 0:
                        dictionary['last_month']['time_of_day_graph']['graph'][time_block_index] += order.quantity
                    
                    # ORDERS FROM LAST 7 DAYS
                    if 1 <= days_ago <= 7:
                        dictionary['weekly_sales']['sales'] += order.total_sale
                        dictionary['total_sales_last_week']['count'] += order.quantity
                        dictionary['total_sales_last_week']['sales'] += order.total_sale
                        dictionary['total_sales_last_week']['graph'][order.date.weekday()] += order.quantity
                        dictionary['last_week']['daily_graph']['graph'][days_ago-1] += order.quantity
                        dictionary['last_week']['weekday_count_graph']['graph'][order.date.weekday()] += order.quantity
                        helper['daily_average']['count_list'][days_ago-1] += order.quantity
                        if time_block_index < 16:
                            dictionary['last_week']['time_of_day_graph']['graph'][time_block_index] += order.quantity
                    
                    # ORDERS FROM 7 DAYS BEFORE
                    if 8 <= days_ago <= 14:
                        helper['weekly_sales']['previous_week'] += order.total_sale
                        helper['total_sales_last_week']['count'] += order.quantity
                        helper['daily_average']['previous_week_count'][days_ago-8] += order.quantity
            
                # ORDER FROM 30 DAYS BEFORE
                if 31 <= days_ago <= 60:
                    helper['monthly_sales']['previous_month'] += order.total_sale
                    helper['daily_average']['previous_month_count'][days_ago-1] += order.quantity
            
            # Label Creation
            dictionary['total_sales_last_week']['labels'] = [calendar.day_name[(today - timedelta(days=i)).weekday()] for i in range(1, 8)]
            
            # POST LOOP CALCULATIONS
            dictionary['weekly_sales']['percentage'] = percent_increase(dictionary['weekly_sales']['sales'], helper['weekly_sales']['previous_week'])
            dictionary['monthly_sales']['percentage'] = percent_increase(dictionary['monthly_sales']['sales'], helper['monthly_sales']['previous_month'])
            dictionary['total_sales_last_week']['arrow_boolean'] = 1 if dictionary['total_sales_last_week']['count'] > helper['total_sales_last_week']['count'] else 0
            dictionary['daily_average']['count'] = average(helper['daily_average']['count_list'])
            dictionary['daily_average']['percentage']['previous_week'] = percent_increase(dictionary['daily_average']['count'], average(helper['daily_average']['previous_week_count']))
            dictionary['daily_average']['percentage']['previous_month'] = percent_increase(dictionary['daily_average']['count'], average(helper['daily_average']['previous_month_count']))
            
            # Reversing lists to get oldests dates on the left
            dictionary['total_sales_last_week']['graph'].reverse()
            dictionary['total_sales_last_week']['labels'].reverse()
            dictionary['last_week']['daily_graph']['graph'].reverse()
            dictionary['last_month']['daily_graph']['graph'].reverse()
            dictionary['last_3_months']['daily_graph']['graph'].reverse()
        
        calc_items_stats(both_items_stats, OrderLine.objects.filter(date__gte=today - relativedelta(days=90), name=item_name).order_by('-date'))
        calc_items_stats(bakery_items_stats, OrderLine.objects.filter(location=CONFIG['BAKERY_ID'], date__gte=today - relativedelta(days=90), name=item_name).order_by('-date'))
        calc_items_stats(cafe_items_stats, OrderLine.objects.filter(location=CONFIG['CAFE_ID'], date__gte=today - relativedelta(days=90), name=item_name).order_by('-date'))