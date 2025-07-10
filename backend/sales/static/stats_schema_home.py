from decimal import Decimal

home_stats = {
    'year_sales_graph': {
        'total_sales_year': Decimal('0.00'),
        'monthly_average': Decimal('0.00'),
        'graph': {},
        'labels': []  
    },
    'average_growth_graph': {
        'average_growth': Decimal('0.00'),
        'percentages': {
            'previous_week': 0,
            'previous_year': 0
        },
        'graph': [Decimal('0.00')] * 7,
        'labels': [],
        'previous_3_weeks': {
            'week0': Decimal('0.00'),
            'week1': Decimal('0.00')
        },
    },
    'monthly_sales_graph': {
        'total_sales_month': Decimal('0.00'),
        'percentages': {
            'previous_month': 0,
            'previous_year': 0
        },
        'graph': [0] * 30
    },
    'monthly_stats_tiles': {
        'total_sales_month': Decimal('0.00'),
        'net_sales_month': Decimal('0.00'),
        'average_sale_month': Decimal('0.00'),
        'items_sold': 0  
    },
    'best_sellers': {
        'yesterday': {
            'names': [],
            'sales': [],
            'counts': [],
            'percentages': [Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00')]
        },
        'last_week': {
            'names': [],
            'sales': [],
            'counts': [],
            'percentages': [Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00')]
        }
    },
    'daily_home_stats': {
        'orders': 0,
        'total_sales': Decimal('0.00'),
        'discounts': Decimal('0.00'),
        'average_sale': Decimal('0.00'),
        'net_sale': Decimal('0.00'),
        'service_charge': Decimal('0.00') ,
    },
}