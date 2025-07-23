from django.core.management.base import BaseCommand
from sales.models import OrderLine
from sales.services.fetch_orders_all import fetch_orders_all

class Command(BaseCommand):
    help = 'Loads Square order date into the datebase from first day of previous month last year (roughly 13 months)'
    
    def handle(self, *args, **options):
        orders = fetch_orders_all()
        if orders:
            self.stdout.write(self.style.SUCCESS('Successfully fetched order, importing data now...'))
        counter = 0
        
        for order in orders:
            if not order.line_items:
                continue
            for item in order.line_items:
                OrderLine.objects.create(
                    name=item.name or 'Custom',
                    quantity=int(item.quantity) if item.quantity else 1,
                    location=order.location_id,
                    date=order.created_at[:10],
                    time=order.created_at[11:16],
                    tax=round(item.total_tax_money.amount / 100, 2) if item.total_tax_money.amount else 0,
                    discount=round(item.total_discount_money.amount / 100, 2) if item.total_discount_money.amount else 0,
                    service_charge=round((order.total_service_charge_money.amount // len(order.line_items)) / 100, 2) if order.total_service_charge_money.amount else 0,
                    total_sale=round(item.total_money.amount / 100, 2) if item.total_money.amount else 0,
                )
                counter += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {counter} order lines.'))
        