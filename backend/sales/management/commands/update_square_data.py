from django.core.management.base import BaseCommand
from sales.models import OrderLine
from sales.services.fetch_orders_new import fetch_orders_new
from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = "Fetches new Square orders and removes data older than the cutoff date (1st of the previous month last year)"
    
    def handle(self, *args, **options):
        cutoff_date = (datetime.now(UTC).date() - relativedelta(years=1, months=1)).replace(day=1)
        
        old_entries = OrderLine.objects.filter(date__lt=cutoff_date)
        count_deleted = old_entries.count()
        old_entries.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count_deleted} old order lines.'))
        
        orders = fetch_orders_new()
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
                    total_sale=round(item.total_money.amount / 100, 2) if item.total_money.amount else 0
                )
                counter += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {counter} new order lines.'))