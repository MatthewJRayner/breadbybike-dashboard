from square import Square
from square.environment import SquareEnvironment
from sales.models import OrderLine
from datetime import datetime, UTC, timedelta
from dateutil.relativedelta import relativedelta
from sales.config import CONFIG

def fetch_orders_all():
    """ Returns all orders from first day of previous month last year (roughly 13 months)"""
    order_entries = []
    client = Square(
        environment=SquareEnvironment.PRODUCTION,
        token=CONFIG['SQUARE_ACCESS_TOKEN']
    )
    end_date = datetime.now(UTC).date()
    start_date = (end_date - relativedelta(years=1, months=1)).replace(day=1)
    
    delta_days = (end_date - start_date).days + 1
    for i in range(delta_days):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.isoformat()
        start_at = f"{date_str}{CONFIG['SQUARE_API_START_TIME']}"
        end_at = f"{date_str}{CONFIG['SQUARE_API_END_TIME']}"
        
        cursor = None
        while True:
            order_response = client.orders.search(
                location_ids = [CONFIG['BAKERY_ID'], CONFIG['CAFE_ID']],
                query={
                    'filter': {
                        'date_time_filter': {
                            'created_at': {
                                'end_at': end_at,
                                'start_at': start_at
                            }
                        },
                        'state_filter': {
                            'states': [ 
                                'COMPLETED'
                            ] 
                        }
                    }
                },
                limit=1000
            )
            
            orders = order_response.orders or []
            order_entries.extend(orders)
            
            cursor = order_response.cursor
            if not cursor:
                break
        
    return order_entries
                
        