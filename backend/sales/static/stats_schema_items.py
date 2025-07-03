from decimal import Decimal
from datetime import time

items_stats = {
    'weekly_sales': {
        'sales': Decimal('0.00'),
        'percentage': 0
    },
    'monthly_sales': {
        'sales': Decimal('0.00'),
        'percentage': 0  
    },
    'total_sales_last_week': {
        'count': 0,
        'arrow_boolean': 1,
        'sales': Decimal('0.00'),
        'graph': [0] * 7,
        'labels': []
    },
    'daily_average': {
        'count': 0,
        'percentage': {
            'previous_week': 0,
            'previous_month': 0,
        }
    },
    'period_graphs': {
        'last_week': {
            'weekday_count_graph': {
                'graph': [0] * 7,
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            'time_of_day_graph': {
                'graph': [0] * 16,
                'labels': ['8:00-8:30', '8:30-9:00', '9:00-9:30', '9:30-10:00', '10:00-10:30', '10:30-11:00', '11:00-11:30', '11:30-12:00', '12:00-12:30', '12:30-13:00', '13:00-13:30', '13:30-14:00', '14:00-14:30', '14:30-15:00', '15:00-15:30', '15:30-16:00']
            },
            'daily_graph': {
                'graph': [0] * 7
            },    
        },
        'last_month': {
            'weekday_count_graph': {
                'graph': [0] * 7,
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            'time_of_day_graph': {
                'graph': [0] * 16,
                'labels': ['8:00-8:30', '8:30-9:00', '9:00-9:30', '9:30-10:00', '10:00-10:30', '10:30-11:00', '11:00-11:30', '11:30-12:00', '12:00-12:30', '12:30-13:00', '13:00-13:30', '13:30-14:00', '14:00-14:30', '14:30-15:00', '15:00-15:30', '15:30-16:00']
            },
            'daily_graph': {
                'graph': [0] * 30
            },     
        },
        'last_3_months': {
            'weekday_count_graph': {
                'graph': [0] * 7,
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            'time_of_day_graph': {
                'graph': [0] * 16,
                'labels': ['8:00-8:30', '8:30-9:00', '9:00-9:30', '9:30-10:00', '10:00-10:30', '10:30-11:00', '11:00-11:30', '11:30-12:00', '12:00-12:30', '12:30-13:00', '13:00-13:30', '13:30-14:00', '14:00-14:30', '14:30-15:00', '15:00-15:30', '15:30-16:00']
            },
            'daily_graph': {
                'graph': [0] * 90
            },     
        },
    },
    'daily_items_stats': {
        'daily_sales': {
            'sales': Decimal('0.00'),
            'percentage': 0
        },
        'recent_time': time(8, 0, 0),
    },
}