from django.core.management.base import BaseCommand
from sales.models import OrderLine, DailyOrderSnapshot
from sales.services.fetch_orders_new import fetch_orders_new
from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = "Fetch and update order lines from Square, clean up old entries, and updates daily snapshots."

    def handle(self, *args, **options):
        cutoff_date_OrderLine = (datetime.now(UTC).date() - relativedelta(years=1, months=1)).replace(day=1)
        
        old_entries_OrderLine = OrderLine.objects.filter(date__lt=cutoff_date_OrderLine)
        count_deleted = old_entries_OrderLine.count()
        old_entries_OrderLine.delete()
        OrderLine.objects.filter(date=datetime.now(UTC).date()).delete()  # Delete today's entries to avoid duplicates
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
        
        # Add / delete orders for DailyOrderSnapshot
        DailyOrderSnapshot.objects.all().delete()
        
        yesterday_orders = OrderLine.objects.filter(date=(datetime.now(UTC).date() - relativedelta(days=1)))
        for order in yesterday_orders:
            DailyOrderSnapshot.objects.create(
                name=order.name,
                date=order.date,
                time=order.time,
                location=order.location,
                quantity=order.quantity,
                total_sale=order.total_sale,
                discount=order.discount,
                service_charge=order.service_charge
            )
            
        previous_week_orders = OrderLine.objects.filter(date=(datetime.now(UTC).date() - relativedelta(days=7)))
        for order in previous_week_orders:
            DailyOrderSnapshot.objects.create(
                name=order.name,
                date=order.date,
                time=order.time,
                location=order.location,
                quantity=order.quantity,
                total_sale=order.total_sale,
                discount=order.discount,
                service_charge=order.service_charge
            )   
            
        self.stdout.write(self.style.SUCCESS(f'Successfully cleared and updated DailyOrderSnapshot'))