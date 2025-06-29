from django.core.management.base import BaseCommand
from sales.models import OrderLine
import json
from datetime import datetime, UTC, timedelta
import calendar
import copy
from dateutil.relativedelta import relativedelta
from sales.static.stats_schema_items import stats
from config import CONFIG

class Command(BaseCommand):
    help = "Computes and stores precomputed stats for the frontend | Clarity prioritized over efficiency as this script will run overnight automatically"
    
    def handle(self, *args, **options):
        # Time based constants and variables
        today = datetime.now(UTC).date()
        current_month = today.month
        current_year = today.year
        last_year_end = today - relativedelta(years=1, days=1)
        current_month = today.month
        # Initializes dictionaries from stats schema
        both_items_stats = {k: v.copy() for k, v in stats.items()}
        bakery_items_stats = {k: v.copy() for k, v in stats.items()}
        cafe_items_stats = {k: v.copy() for k, v in stats.items()}
        helper = {
            'weekly_sales': {
                'previous_week': 0.00
            },
            'monthly_sales': {
                'previous_month': 0.00
            },
            'total_sales_last_week': {
                'count_previous_week': 0,
                'previous_week_sales': 0.00
            },
        }