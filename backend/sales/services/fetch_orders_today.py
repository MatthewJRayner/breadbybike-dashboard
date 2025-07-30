from square import Square
from square.environment import SquareEnvironment
from sales.models import OrderLine, DailyOrderSnapshot
from datetime import datetime, timedelta, UTC
from dateutil.relativedelta import relativedelta
from django.conf import settings

def fetch_orders_today():
    """ Returns all orders since the most recent time in the database until now"""
    client = Square(
        environment=SquareEnvironment.PRODUCTION,
        token=settings.CONFIG['SQUARE_ACCESS_TOKEN']
    )
    
    today = datetime.now(UTC)
    start_at = f'{today.date()}T00:00:00.000Z'
    end_at = f'{today.date()}T23:59:59.000Z'
    
    order_entries = []
    cursor = None
    while True:
        order_response = client.orders.search(
            location_ids=[settings.CONFIG['BAKERY_ID'], settings.CONFIG['CAFE_ID']],
            query={
                'filter': {
                    'date_time_filter': {
                        'created_at': {
                            'start_at': start_at,
                            'end_at': end_at
                        }
                    },
                    'state_filter': {
                        'states': ['COMPLETED']
                    }
                }
            },
            limit=1000,
            cursor=cursor
        )
        
        orders = order_response.orders or []
        order_entries.extend(orders)
        
        cursor = order_response.cursor
        if not cursor:
            break
    
    return order_entries