from django.core.management.base import BaseCommand
from sales.models import OrderLine
import json
from datetime import datetime, UTC, timedelta
import calendar
import copy
from dateutil.relativedelta import relativedelta
from sales.static.stats_schema_home import stats
from config import CONFIG

class Command(BaseCommand):
    help = "Computes and stores precomputed stats for the frontend | Clarity prioritzed over efficiency as this script will run overnight automatically"
    
    def handle(self, *args, **options):
        # Time based constants and variables
        today = datetime.now(UTC).date()
        current_month = today.month
        current_year = today.year
        last_year_end = today - relativedelta(years=1, days=1)
        current_month = today.month
        # Initializes dictionaries from stats schema
        both_home_stats = {k: v.copy() for k, v in stats.items()}
        bakery_home_stats = {k: v.copy() for k, v in stats.items()}
        cafe_stats_calc = {k: v.copy() for k, v in stats.items()} 
        helper = {
            'average_growth_graph': {
                'previous_7_days': {f'{i}': 0.00 for i in range(1, 8)},
                'previous_14_days': {f'{i}': 0.00 for i in range(1, 8)},
                'previous_21_days': {f'{i}': 0.00 for i in range(1, 8)},
                'previous_28_days': {f'{i}': 0.00 for i in range(1, 8)},
                'same_period_last_year': {f'{i}': 0.00 for i in range(1, 8)},
                'same_period_last_year_week_before': {f'{i}': 0.00 for i in range(1, 8)},
                'comparisons': {
                    'previous_14_days': [0.00] * 7,
                    'previous_21_days': [0.00] * 7,
                    'same_period_last_year': [0.00] * 7   
                },
                'percentages': {
                    'previous_year': 0
                }
            },
            'monthly_sales_graph': {
                'previous_month_sales': 0.00,
                'same_month_previous_year': 0.00,
            },
            'monthly_stats_tiles': {
                'total_lost': 0.00
            },
        }
        
        # Functions
        def percent_increase(a, b):
            """ Returns the percent increase of two numbers, with a being the end variable and b being the original variable """
            return 0.00 if b == 0 else round(((a - b) / b) * 100, 2)
        
        
        def average(a):
            """ Returns the average of a list of numbers """
            return sum(a) / len(a) if a else 0.00
        
        
        def calc_home_stats(dictionary, querylist):
            """ Take premade dictionary and calculates required values """
            # Creat correct amount of keys for graph dictionaries
            dictionary['year_sales_graph']['graph'] = {f'month{i}': 0.00 for i in range(1, current_month + 1)}
            
            # Big for loop to add data incrementally
            for order in querylist:
                days_ago = (today - order.date).days
                same_period_last_year = days_ago - (today-last_year_end).days()
                
                # CURRENT YEARS ORDERS
                if order.date.year == today.year:
                    dictionary['year_sales_graph']['total_sales'] += order.total_sale
                    # CURRENT MONTH ORDERS
                    if order.date.month == current_month:
                        dictionary['monthly_stats_tiles']['total_sales_month'] += order.total_sale
                        dictionary['monthly_stats_tiles']['item_sold'] += int(order.quantity)
                        helper['monthly_stats_tiles']['total_lost'] += (order.tax + order.discount + order.service_charge)
                    
                    if order.date.month == current_month - 1:
                        helper['monthly_sales_graph']['previous_month_sales'] += order.total_sale
                    
                    # ORDER TAKEN FROM EVERY MONTH CURRENT YEAR
                    dictionary['year_sales_graph']['graph'][f'month{order.date.month}'] += order.total_sale
                    
                # PREVIOUS 30 DAYS ORDERS
                if 1 <= days_ago <= 30:
                    dictionary['monthly_sales_graph']['total_sales_month'] += order.total_sale
                    dictionary['monthly_sales_grapgh']['graph'][days_ago - 1] += order.total_sale
                    if 1 <= days_ago <= 7:
                        helper['average_growth_graph']['previous_7_days'][f'{days_ago}'] += order.total_sale
                    if 8 <= days_ago <= 14:
                        helper['average_growth_graph']['previous_14_days'][f'{days_ago - 7}'] += order.total_sale  
                    if 15 <= days_ago <= 21:
                        helper['average_growth_graph']['previous_21_days'][f'{days_ago - 14}'] += order.total_sale
                    if 22 <= days_ago <= 28:
                        helper['average_growth_graph']['previous_28_days'][f'{days_ago - 21}'] += order.total_sale
                    
                # 30 DAYS BEFORE PREVIOUS 30 DAYS ORDERS
                if 31 <= days_ago <= 60:
                    helper['monthly_sales_graph']['previous_month_sales'] += order.total_sale
                
                # SAME PERIOD LAST YEAR 30 DAYS ORDERS
                if 1 <= same_period_last_year <= 30:
                    helper['monthly_sales_graph']['same_month_previous_year'] += order.total_sale
                    if 1 <= same_period_last_year <= 7:
                        helper['average_growth_graph']['same_period_last_year'][f'{same_period_last_year}'] += order.total_sale
                    if 8 <= same_period_last_year <= 14:
                        helper['average_growth_graph']['same_period_last_year_week_before'][f'{same_period_last_year}'] += order.total_sale
                
            # Label Creation
            for i in range(1, current_month + 1):
                dictionary['year_sales_graph']['labels'].append(f"{calendar.month_abbr[i]} '{today.strftime('%y')}")
            dictionary['year_sales_graph']['labels'].reverse()
            
            for i in range(7):
                day = today - timedelta(days=i+1)
                dictionary['average_growth_graph']['labels'].append(calendar.day_abbr(day.weekday()))
                dictionary['average_growth_graph']['graph'][i] = percent_increase(helper['average_growth_graph']['previous_7_days'][f'{i}'], helper['average_growth_graph']['previous_14_days'][f'{i}'])
                helper['average_growth_graph']['comparisons']['previous_14_days'][i] = percent_increase(helper['average_growth_graph']['previous_14_days'][f'{i}'], helper['average_growth_graph']['previous_21_days'][f'{i}'])
                helper['average_growth_graph']['comparisons']['previous_21_days'][i] = percent_increase(helper['average_growth_graph']['previous_21_days'][f'{i}'], helper['average_growth_graph']['previous_28_days'][f'{i}'])
                helper['average_growth_graph']['comparisons']['same_period_last_year'][i] = percent_increase(helper['average_growth_graph']['same_period_last_year'][f'{i}'], helper['average_growth_graph']['same_period_last_year_week_before'][f'{i}'])
                
            # Post for loop calculations
            dictionary['year_sales_graph']['monthly_average'] = round(dictionary['year_sales_graph']['total_sales'] / current_month, 2)
            dictionary['average_growth_graph']['average_growth'] = round(average(dictionary['average_growth_graph']['graph']), 2)
            helper['average_growth_graph']['percentages']['previous_year'] = average(helper['average_growth_graph']['comparisons']['same_period_last_year'])
            dictionary['average_growth_graph']['previous_3_weeks']['week0'] = round(average(helper['average_growth_graph']['comparisons']['previous_14_days']), 2)
            dictionary['average_growth_graph']['previous_3_weeks']['week1'] = round(average(helper['average_growth_graph']['comparisons']['previous_21_days']), 2)
            dictionary['average_growth_graph']['percentages']['previous_week'] = round(percent_increase(dictionary['average_growth_graph']['average_growth'], dictionary['average_growth_graph']['previous_3_weeks']['week0']))
            dictionary['average_growth_graph']['percentages']['previous_year'] = round(percent_increase(dictionary['average_growth_graph']['average_growth'], helper['average_growth_graph']['percentages']['previous_year']))    
            dictionary['monthly_sales_graph']['percentages']['previous_month'] = round(percent_increase(dictionary['monthly_sales_graph']['total_sales_month'], helper['monthly_sales_graph']['previous_month_sales']))
            dictionary['monthly_sales_graph']['percentages']['previous_year'] = round(percent_increase(dictionary['monthly_sales_graph']['total_sales_month'], helper['monthly_sales_graph']['same_month_previous_year']))
            dictionary['monthly_stats_tiles']['net_sales_month'] = dictionary['monthly_stats_tiles']['total_sales_month'] - helper['monthly_stats_tiles']['total_lost']
            dictionary['monthly_stats_tiles']['average_sale_month'] = round(dictionary['monthly_stats_tiles']['total_sales_month'] / dictionary['monthly_stats_tiles']['items_sold'], 2)
            
        calc_home_stats(both_home_stats, OrderLine.objects.all().order_by('-date'))
        calc_home_stats(bakery_home_stats, OrderLine.objects.filter(location=CONFIG['BAKERY_ID']).order_by('-date'))
        calc_home_stats(cafe_stats_calc, OrderLine.objects.filter(location=CONFIG['CAFE_ID']).order_by('-date'))