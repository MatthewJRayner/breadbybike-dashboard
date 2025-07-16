from django.core.management.base import BaseCommand
from sales.models import ShopifyOrders
from sales.services.fetch_shopify_orders import fetch_shopify_orders
from datetime import datetime, UTC, timedelta

class Command(BaseCommand):
    help = "Fetches pickup orders from shopify API and adds relevant information to ShopifyOrders model"
    
    def handle(self, *args, **options):
        cutoff_date = datetime.now(UTC).date()
        ShopifyOrders.objects.filter(delivery_date__lt=cutoff_date).delete()
        
        orders = fetch_shopify_orders()
        counter = 0
        for order in orders:
            method = order.get('shipping_lines', [{}])[0].get('title', '')
            order_id = order['order_number']
            delivery = order.get('note_attributes', [{}])[1].get('value', '')
            
            if not ShopifyOrders.objects.filter(order_id=order_id).exists():
                ShopifyOrders.objects.create(
                    order_id=order_id,
                    delivery_date=datetime.strptime(delivery, '%Y/%m/%d').date(),
                    customer_name_first=order.get('customer', {}).get('first_name', ''),
                    customer_name_last=order.get('customer', {}).get('last_name', ''),
                    line_items=order.get('line_items', []),
                    notes=order.get('note', ''),
                    method=method
                )
            counter += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {counter} new order lines.'))