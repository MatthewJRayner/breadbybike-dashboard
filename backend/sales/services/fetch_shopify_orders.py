import requests
import json
from sales.config import CONFIG
from datetime import datetime, UTC, timedelta


def fetch_shopify_orders():
    # CONSTANTS
    yesterday = datetime.now(UTC) - timedelta(days=1)
    date_min = yesterday.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    date_max = yesterday.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    # API Request args
    params = {
        'status': 'any',
        'created_at_min': date_min,
        'created_at_max': date_max,
        'limit': 250
    }
    headers = {
        'X-Shopify-Access-Token': CONFIG['SHOPIFY_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    url = f"https://{CONFIG['SHOPIFY_SHOP_URL']}/admin/api/{CONFIG['SHOPIFY_API_VERSION']}/orders.json"

    # Request and filtering
    pickup_orders = []
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        orders = response.json()['orders']
        for order in orders:
            for shipping_line in order.get('shipping_lines', []):
                if 'pickup' in shipping_line.get('code', '').lower():
                    pickup_orders.append(order)
                    break
        return pickup_orders
    else:
        return []
    