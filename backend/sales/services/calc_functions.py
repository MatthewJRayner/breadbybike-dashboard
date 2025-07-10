from datetime import datetime, UTC, timedelta, time
import calendar
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from sales.static.stats_schema_home import home_stats
from sales.static.stats_schema_items import items_stats
from sales.config import CONFIG

# VARIABLES AND CONSTANTS
today = datetime.now(UTC).date()
current_month = today.month
last_year_end = today - relativedelta(years=1, days=1)
start_time = time(hour=7, minute=0, second=0)
time_now = datetime.now(UTC).time()
best_sellers_list_size = 5

# FUNCTIONS

def percent_increase(a, b):
    """ Returns the percent increase of two numbers, with a being the end variable and b being the original variable """
    return Decimal('0.00') if b == 0 else round(((a - b) / b) * 100, 2)


def average(a):
    """ Returns the average of a list of numbers """
    return sum(a) / len(a) if a else Decimal('0.00')


def convert_to_serializable(obj):
    """ Converts Decimal objects to float for JSON serialization """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, time):
        return obj.strftime('%H:%M:%S')
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(v) for v in obj]
    return obj


def convert_from_serializable(obj):
    """ Converts float objects back to Decimal for internal use """
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_from_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_from_serializable(v) for v in obj]
    return obj


def calc_home_stats(dictionary, querylist):
    """ Take premade dictionary and calculates required values """
    
    # Initialize helper dictionary
    helper = {
        'average_growth_graph': {
            'previous_7_days': [Decimal('0.00')] * 7,
            'previous_14_days': [Decimal('0.00')] * 7,
            'previous_21_days': [Decimal('0.00')] * 7,
            'previous_28_days': [Decimal('0.00')] * 7,
            'same_period_last_year': [Decimal('0.00')] * 7,
            'same_period_last_year_week_before': [Decimal('0.00')] * 7,
            'comparisons': {
                'previous_14_days': [Decimal('0.00')] * 7,
                'previous_21_days': [Decimal('0.00')] * 7,
                'same_period_last_year': [Decimal('0.00')] * 7   
            },
            'percentages': {
                'previous_year': 0
            }
        },
        'monthly_sales_graph': {
            'previous_month_sales': Decimal('0.00'),
            'same_month_previous_year': Decimal('0.00'),
        },
        'monthly_stats_tiles': {
            'total_lost': Decimal('0.00')
        },
        'previous_week_sales': {
            'sales': Decimal('0.00')
        },
        'same_week_previous_year': {
            'sales': Decimal('0.00')
        },
        'weekly_sales': {
            'sales': Decimal('0.00')
        },
        'best_sellers_stats': {
            'yesterday': {
                'sales': Decimal('0.00'),
                'count': 0,
                'best_sellers': {}    
            },
            'previous_week': {
                'sales': Decimal('0.00'),
                'count': 0,
                'best_sellers': {}
            }
        }
    }
    
    # Creat correct amount of keys for graph dictionaries
    dictionary['year_sales_graph']['graph'] = {f'month{i}': Decimal('0.00') for i in range(1, current_month + 1)}
    
    # Big for loop to add data incrementally
    for order in querylist:
        days_ago = (today - order.date).days
        same_period_last_year = days_ago - (today-last_year_end).days
        
        # CURRENT YEARS ORDERS
        if order.date.year == today.year:
            dictionary['year_sales_graph']['total_sales_year'] += order.total_sale
            # CURRENT MONTH ORDERS
            if order.date.month == current_month:
                dictionary['monthly_stats_tiles']['total_sales_month'] += order.total_sale
                dictionary['monthly_stats_tiles']['items_sold'] += int(order.quantity)
                helper['monthly_stats_tiles']['total_lost'] += (order.tax + order.discount + order.service_charge)
            
            if order.date.month == current_month - 1:
                helper['monthly_sales_graph']['previous_month_sales'] += order.total_sale
            
            # ORDER TAKEN FROM EVERY MONTH CURRENT YEAR
            dictionary['year_sales_graph']['graph'][f'month{order.date.month}'] += order.total_sale
            
        # PREVIOUS 30 DAYS ORDERS
        if 1 <= days_ago <= 30:
            dictionary['monthly_sales_graph']['total_sales_month'] += order.total_sale
            dictionary['monthly_sales_graph']['graph'][days_ago - 1] += order.total_sale
            if 1 <= days_ago <= 7:
                if days_ago == 1:
                    helper['best_sellers_stats']['yesterday']['sales'] += order.total_sale
                    if order.name in helper['best_sellers_stats']['yesterday']['best_sellers']:
                        helper['best_sellers_stats']['yesterday']['best_sellers'][order.name]['sales'] += order.total_sale
                        helper['best_sellers_stats']['yesterday']['best_sellers'][order.name]['count'] += order.quantity
                    else:
                        helper['best_sellers_stats']['yesterday']['best_sellers'][order.name] = {
                            'sales': order.total_sale,
                            'count': order.quantity
                        }
                helper['weekly_sales']['sales'] += order.total_sale
                helper['previous_week_sales']['sales'] += order.total_sale
                helper['average_growth_graph']['previous_7_days'][days_ago - 1] += order.total_sale
                helper['best_sellers_stats']['previous_week']['sales'] += order.total_sale
                if order.name in helper['best_sellers_stats']['previous_week']['best_sellers']:
                    helper['best_sellers_stats']['previous_week']['best_sellers'][order.name]['sales'] += order.total_sale
                    helper['best_sellers_stats']['previous_week']['best_sellers'][order.name]['count'] += order.quantity
                else:
                    helper['best_sellers_stats']['previous_week']['best_sellers'][order.name] = {
                        'sales': order.total_sale,
                        'count': order.quantity
                    }
                
            if 8 <= days_ago <= 14:
                helper['average_growth_graph']['previous_14_days'][days_ago - 8] += order.total_sale  
            if 15 <= days_ago <= 21:
                helper['average_growth_graph']['previous_21_days'][days_ago - 15] += order.total_sale
            if 22 <= days_ago <= 28:
                helper['average_growth_graph']['previous_28_days'][days_ago - 22] += order.total_sale
            
        # 30 DAYS BEFORE PREVIOUS 30 DAYS ORDERS
        if 31 <= days_ago <= 60:
            helper['monthly_sales_graph']['previous_month_sales'] += order.total_sale
        
        # SAME PERIOD LAST YEAR 30 DAYS ORDERS
        if same_period_last_year > 0 and same_period_last_year <= 30:
            helper['monthly_sales_graph']['same_month_previous_year'] += order.total_sale
            if 1 <= same_period_last_year <= 7:
                helper['same_week_previous_year']['sales'] += order.total_sale
                helper['average_growth_graph']['same_period_last_year'][same_period_last_year - 1] += order.total_sale
            if 8 <= same_period_last_year <= 14:
                helper['average_growth_graph']['same_period_last_year_week_before'][same_period_last_year - 8] += order.total_sale
        
    # Label Creation
    for i in range(1, current_month + 1):
        dictionary['year_sales_graph']['labels'].append(f"{calendar.month_abbr[i]} '{today.strftime('%y')}")
    
    for i in range(7):
        day = today - timedelta(days=i+1)
        dictionary['average_growth_graph']['labels'].append(calendar.day_abbr[day.weekday()])
        dictionary['average_growth_graph']['graph'][i] = percent_increase(helper['average_growth_graph']['previous_7_days'][i], helper['average_growth_graph']['previous_14_days'][i])
        helper['average_growth_graph']['comparisons']['previous_14_days'][i] = percent_increase(helper['average_growth_graph']['previous_14_days'][i], helper['average_growth_graph']['previous_21_days'][i])
        helper['average_growth_graph']['comparisons']['previous_21_days'][i] = percent_increase(helper['average_growth_graph']['previous_21_days'][i], helper['average_growth_graph']['previous_28_days'][i])
        helper['average_growth_graph']['comparisons']['same_period_last_year'][i] = percent_increase(helper['average_growth_graph']['same_period_last_year'][i], helper['average_growth_graph']['same_period_last_year_week_before'][i])
        
    # Post for loop calculations
    dictionary['year_sales_graph']['monthly_average'] = round(average(list(dictionary['year_sales_graph']['graph'].values())[:current_month-1]), 2)
    dictionary['average_growth_graph']['average_growth'] = round(average(dictionary['average_growth_graph']['graph']), 2)
    helper['average_growth_graph']['percentages']['previous_year'] = average(helper['average_growth_graph']['comparisons']['same_period_last_year'])
    dictionary['average_growth_graph']['previous_3_weeks']['week0'] = round(average(helper['average_growth_graph']['comparisons']['previous_14_days']), 2)
    dictionary['average_growth_graph']['previous_3_weeks']['week1'] = round(average(helper['average_growth_graph']['comparisons']['previous_21_days']), 2)
    dictionary['average_growth_graph']['percentages']['previous_week'] = round(percent_increase(helper['weekly_sales']['sales'], helper['previous_week_sales']['sales']))
    dictionary['average_growth_graph']['percentages']['previous_year'] = round(percent_increase(helper['weekly_sales']['sales'], helper['same_week_previous_year']['sales']))    
    dictionary['monthly_sales_graph']['percentages']['previous_month'] = round(percent_increase(dictionary['monthly_sales_graph']['total_sales_month'], helper['monthly_sales_graph']['previous_month_sales']))
    dictionary['monthly_sales_graph']['percentages']['previous_year'] = round(percent_increase(dictionary['monthly_sales_graph']['total_sales_month'], helper['monthly_sales_graph']['same_month_previous_year']))
    dictionary['monthly_stats_tiles']['net_sales_month'] = dictionary['monthly_stats_tiles']['total_sales_month'] - helper['monthly_stats_tiles']['total_lost']
    dictionary['monthly_stats_tiles']['average_sale_month'] = round(dictionary['monthly_stats_tiles']['total_sales_month'] / dictionary['monthly_stats_tiles']['items_sold'], 2) if dictionary['monthly_stats_tiles']['items_sold'] else Decimal('0.00')
    top_sellers_yesterday = sorted(helper['best_sellers_stats']['yesterday']['best_sellers'].items(), key=lambda x: x[1]['sales'], reverse=True)[:best_sellers_list_size]
    for k, v in top_sellers_yesterday:
        dictionary['best_sellers']['yesterday']['names'].append(k)
        dictionary['best_sellers']['yesterday']['sales'].append(v['sales'])
        dictionary['best_sellers']['yesterday']['counts'].append(v['count'])
    top_sellers_previous_week = sorted(helper['best_sellers_stats']['previous_week']['best_sellers'].items(), key=lambda x: x[1]['sales'], reverse=True)[:best_sellers_list_size]
    for k, v in top_sellers_previous_week:
        dictionary['best_sellers']['last_week']['names'].append(k)
        dictionary['best_sellers']['last_week']['sales'].append(v['sales'])
        dictionary['best_sellers']['last_week']['counts'].append(v['count'])
    for i in range(best_sellers_list_size):
        dictionary['best_sellers']['yesterday']['percentages'][i] = round((
            dictionary['best_sellers']['yesterday']['sales'][i] / helper['best_sellers_stats']['yesterday']['sales'] if helper['best_sellers_stats']['yesterday']['sales'] > 0 else Decimal('1.00')
            ) * 100)
        dictionary['best_sellers']['last_week']['percentages'][i] = round((
            dictionary['best_sellers']['last_week']['sales'][i] / helper['best_sellers_stats']['previous_week']['sales'] if helper['best_sellers_stats']['previous_week']['sales'] > 0 else Decimal('1.00')
            ) * 100)
    
    # Reversing lists to get oldests dates on the left
    dictionary['average_growth_graph']['graph'].reverse()
    dictionary['average_growth_graph']['labels'].reverse()
    dictionary['monthly_sales_graph']['graph'].reverse()


def calc_items_stats(dictionary, querylist):
    """ 
    Calculates the items stats for a given dictionary and querylist. 
    Assuming the querylist is filted to be the last 90 days and by item name
    """
    # Initialize the helper dictionary
    helper = {
        'weekly_sales': {
            'previous_week': Decimal('0.00')
        },
        'monthly_sales': {
            'previous_month': Decimal('0.00')
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

    # Big for loop to iterate through all the items in the querylist
    for order in querylist:
        days_ago = (today - order.date).days
        time_block_index = ((order.time.hour - start_time.hour) * 60 + order.time.minute) // 30
    
        dictionary['period_graphs']['last_3_months']['daily_graph']['graph'][(days_ago - 1) if days_ago > 0 else 0] += order.quantity
        dictionary['period_graphs']['last_3_months']['weekday_count_graph']['graph'][order.date.weekday()] += order.quantity
        if 0 <= time_block_index < 16:
            dictionary['period_graphs']['last_3_months']['time_of_day_graph']['graph'][time_block_index] += order.quantity
        
        # ORDERS FROM LAST 30 DAYS
        if 1 <= days_ago <= 30:
            dictionary['monthly_sales']['sales'] += order.total_sale
            dictionary['period_graphs']['last_month']['daily_graph']['graph'][days_ago-1] += order.quantity
            dictionary['period_graphs']['last_month']['weekday_count_graph']['graph'][order.date.weekday()] += order.quantity
            helper['monthly_sales']['previous_month'] += order.total_sale
            helper['daily_average']['previous_month_count'][days_ago - 1] += order.quantity
            if 0 <= time_block_index < 16:
                dictionary['period_graphs']['last_month']['time_of_day_graph']['graph'][time_block_index] += order.quantity
            
            # ORDERS FROM LAST 7 DAYS
            if 1 <= days_ago <= 7:
                dictionary['weekly_sales']['sales'] += order.total_sale
                dictionary['total_sales_last_week']['count'] += order.quantity
                dictionary['total_sales_last_week']['sales'] += order.total_sale
                dictionary['total_sales_last_week']['graph'][order.date.weekday()] += order.quantity
                dictionary['period_graphs']['last_week']['daily_graph']['graph'][days_ago-1] += order.quantity
                dictionary['period_graphs']['last_week']['weekday_count_graph']['graph'][order.date.weekday()] += order.quantity
                helper['daily_average']['count_list'][days_ago -1] += order.quantity
                if 0 <= time_block_index < 16:
                    dictionary['period_graphs']['last_week']['time_of_day_graph']['graph'][time_block_index] += order.quantity
            
            # ORDERS FROM 7 DAYS BEFORE
            if 8 <= days_ago <= 14:
                helper['weekly_sales']['previous_week'] += order.total_sale
                helper['total_sales_last_week']['count'] += order.quantity
                helper['daily_average']['previous_week_count'][days_ago-8] += order.quantity
    
        # ORDER FROM 30 DAYS BEFORE
        if 31 <= days_ago <= 60:
            helper['monthly_sales']['previous_month'] += order.total_sale
            helper['daily_average']['previous_month_count'][days_ago-31] += order.quantity
    
    # Label Creation
    dictionary['total_sales_last_week']['labels'] = [calendar.day_name[(today - timedelta(days=i)).weekday()] for i in range(1, 8)]
    
    # POST LOOP CALCULATIONS
    dictionary['weekly_sales']['percentage'] = percent_increase(dictionary['weekly_sales']['sales'], helper['weekly_sales']['previous_week'])
    dictionary['monthly_sales']['percentage'] = percent_increase(dictionary['monthly_sales']['sales'], helper['monthly_sales']['previous_month'])
    dictionary['total_sales_last_week']['arrow_boolean'] = 1 if dictionary['total_sales_last_week']['count'] > helper['total_sales_last_week']['count'] else 0
    dictionary['daily_average']['count'] = round(average(helper['daily_average']['count_list']))
    dictionary['daily_average']['percentage']['previous_week'] = percent_increase(dictionary['daily_average']['count'], average(helper['daily_average']['previous_week_count']))
    dictionary['daily_average']['percentage']['previous_month'] = percent_increase(dictionary['daily_average']['count'], average(helper['daily_average']['previous_month_count']))
    for i in range(16):
        dictionary['period_graphs']['last_week']['time_of_day_graph']['graph'][i] = round(dictionary['period_graphs']['last_week']['time_of_day_graph']['graph'][i] / 7)
        dictionary['period_graphs']['last_month']['time_of_day_graph']['graph'][i] = round(dictionary['period_graphs']['last_month']['time_of_day_graph']['graph'][i] / 30)
        dictionary['period_graphs']['last_3_months']['time_of_day_graph']['graph'][i] = round(dictionary['period_graphs']['last_3_months']['time_of_day_graph']['graph'][i] / 90)
    for i in range(7):
        dictionary['period_graphs']['last_week']['weekday_count_graph']['graph'][i] = round(dictionary['period_graphs']['last_week']['weekday_count_graph']['graph'][i] / 7)
        dictionary['period_graphs']['last_month']['weekday_count_graph']['graph'][i] = round(dictionary['period_graphs']['last_month']['weekday_count_graph']['graph'][i] / 30)
        dictionary['period_graphs']['last_3_months']['weekday_count_graph']['graph'][i] = round(dictionary['period_graphs']['last_3_months']['weekday_count_graph']['graph'][i] / 90)
        
    # Reversing lists to get oldests dates on the left
    dictionary['total_sales_last_week']['graph'].reverse()
    dictionary['total_sales_last_week']['labels'].reverse()
    dictionary['period_graphs']['last_week']['daily_graph']['graph'].reverse()
    dictionary['period_graphs']['last_month']['daily_graph']['graph'].reverse()
    dictionary['period_graphs']['last_3_months']['daily_graph']['graph'].reverse()
    

def calc_daily_stats_home(dictionary, querylist):
    """
    Calculates the stats for home page from the current days orders and yesterdays for the frontend
    """
    # Initialize the helper dictionary
    helper = {
        'tax': Decimal('0.00'),
    }
    
    for order in querylist:
        if order.date == today:
            dictionary['daily_home_stats']['total_sales'] += order.total_sale
            helper['tax'] += order.tax
            dictionary['daily_home_stats']['orders'] += order.quantity
            dictionary['daily_home_stats']['discounts'] += order.discount
            dictionary['daily_home_stats']['service_charge'] += order.service_charge
    
    # Post loop calculations
    dictionary['daily_home_stats']['net_sale'] = dictionary['daily_home_stats']['total_sales'] - (dictionary['daily_home_stats']['discounts'] + dictionary['daily_home_stats']['service_charge'] + helper['tax'])
    dictionary['daily_home_stats']['average_sale'] = round(dictionary['daily_home_stats']['total_sales'] / dictionary['daily_home_stats']['orders'], 2) if dictionary['daily_home_stats']['orders'] else Decimal('0.00')
        
        
def calc_daily_stats_items(dictionary, querylist):
    """
    Calculates the stats for items page from the current days orders and the same day previous week for the frontend
    """
    # Initialize the helper dictionary
    helper = {
        'previous_week': {
            'sales': Decimal('0.00')
        }
    }
    
    for order in querylist:
        if order.date == today:
            dictionary['daily_items_stats']['daily_sales']['sales'] += order.total_sale
        if order.date == today - timedelta(days=1):
            dictionary['daily_items_stats']['recent_time'] = order.time if order.time > time.fromisoformat(str(dictionary['daily_items_stats']['recent_time'])) else dictionary['daily_items_stats']['recent_time']
        if order.date == today - timedelta(days=7) and order.time <= time_now:
            helper['previous_week']['sales'] += order.total_sale
        
    
    # Post loop calculations
    dictionary['daily_items_stats']['daily_sales']['percentage'] = percent_increase(dictionary['daily_items_stats']['daily_sales']['sales'], helper['previous_week']['sales'])
    temp_datetime = datetime.combine(datetime.now(UTC).date(), dictionary['daily_items_stats']['recent_time'])
    dictionary['daily_items_stats']['recent_time'] = (temp_datetime + timedelta(hours=1)).time()