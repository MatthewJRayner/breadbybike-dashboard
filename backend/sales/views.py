import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sales.models import OrderStats, OrderLine, DailyOrderSnapshot
from dateutil.relativedelta import relativedelta
from datetime import datetime, UTC
from sales.services.calc_functions import calc_items_stats, calc_daily_stats_items, convert_to_serializable
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core.management import call_command
from sales.static.stats_schema_items import items_stats
from sales.config import CONFIG
import copy
from square import Square
from square.environment import SquareEnvironment
import os

logger = logging.getLogger('sales')

def home(request):
    return HttpResponse("Django is working!")

# Create your views here.
class OrderStatsView(APIView):
    """
    API view to retrieve stats from OrderStats model based on location and item.
    Query parameters: location (e.g., 'both', 'bakery', 'cafe') and item (e.g., 'Cinnamon', optional).
    """
    def get(self, request):
        location_param = request.query_params.get('locations')
        if not location_param:
            return Response(
                {'error': 'Locations parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        loc_list = [loc.strip() for loc in location_param.split(',')]
        
        try:
            stats = OrderStats.objects.filter(location__in=loc_list)
            if not stats.exists():
                return Response(
                    {'error': f'No stats found for the provided locations {loc_list}.'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            data = {
                stat.location: stat.stats_json for stat in stats
            }
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TriggerCalculationsView(APIView):
    """
    API view to trigger calculation of item statistics based on location and item name.
    Accepts POST requests with 'location' and 'item_name' parameters.
    Uses functions from calc_functions services file that are used for overnight autmated scripts.
    """
    def post(self, request):
        logger.info("TriggerCalculationsView POST request received")
        
        location = request.data.get('location')
        item_name = request.data.get('item_name')
        logger.debug(f"Received location: {location}, item_name: {item_name}")
        poss_locations = ['Both', 'Cafe', 'Bakery']

        if not location or not item_name:
            logger.warning("Missing required parameters: location or item_name")
            return Response({'error': 'Location and item name are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)

        if location not in poss_locations:
            logger.warning(f"Invalid location provided: {location}")
            return Response({'error': 'Invalid location'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item_name = item_name.strip()
        if not item_name:
            logger.warning("Empty item name after stripping")
            return Response({'error': 'Item name cannot be empty'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item_key = f'{location}_items_{item_name}'
        logger.info(f"Processing calculation for: {item_key}")

        try:
            bakery_stats = copy.deepcopy(items_stats)
            cafe_stats = copy.deepcopy(items_stats)
            both_stats = copy.deepcopy(items_stats)
            logger.debug("Initialized stats dictionary")

            # Create filters based on stats from only the last 90 days
            bakery_order_lines = OrderLine.objects.filter(
                name=item_name, 
                location=CONFIG['BAKERY_ID'], 
                date__gte=datetime.now(UTC).date() - relativedelta(days=90)
            )
            cafe_order_lines = OrderLine.objects.filter(
                name=item_name, 
                location=CONFIG['CAFE_ID'], 
                date__gte=datetime.now(UTC).date() - relativedelta(days=90)
            )
            both_order_lines = OrderLine.objects.filter(
                name=item_name,
                date__gte=datetime.now(UTC).date() - relativedelta(days=90)
            )
            bakery_daily_orders = DailyOrderSnapshot.objects.filter(name=item_name, location=CONFIG['BAKERY_ID'])
            cafe_daily_orders = DailyOrderSnapshot.objects.filter(name=item_name, location=CONFIG['CAFE_ID'])
            both_daily_orders = DailyOrderSnapshot.objects.filter(name=item_name)
            
            if bakery_order_lines.exists() and cafe_order_lines.exists() and both_order_lines.exists():
                logger.debug("Calculating items stats from order lines")
                calc_items_stats(bakery_stats, bakery_order_lines)
                calc_items_stats(cafe_stats, cafe_order_lines)
                calc_items_stats(both_stats, both_order_lines)
                
            if bakery_daily_orders.exists() and cafe_daily_orders.exists() and both_daily_orders.exists():
                logger.debug("Calculating daily stats from daily orders")
                calc_daily_stats_items(bakery_stats, bakery_daily_orders)
                calc_daily_stats_items(cafe_stats, cafe_daily_orders)
                calc_daily_stats_items(both_stats, both_daily_orders)
            
            # Update calculated stats in the model
            OrderStats.objects.update_or_create(
                location=f'Bakery_items_{item_name}',
                defaults={'stats_json': convert_to_serializable(bakery_stats)}
            )
            OrderStats.objects.update_or_create(
                location=f'Cafe_items_{item_name}',
                defaults={'stats_json': convert_to_serializable(cafe_stats)}
            )
            OrderStats.objects.update_or_create(
                location=f'Both_items_{item_name}',
                defaults={'stats_json': convert_to_serializable(both_stats)}
            )
            logger.info(f"Successfully saved stats for {item_key}")
            
            return Response({'message': f'Stats calculated for {item_key}'}, 
                           status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing {item_name}: {str(e)}", exc_info=True)
            return Response({'error': f'Error processing {item_name}: {str(e)}'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SquareCatalogItemsView(APIView):
    """
    API View to get the list of all items in the catalog currently.
    This list will be used to get the item name variable in various part's of the code
    """
    def get(self, request):
        client = Square(
            environment=SquareEnvironment.PRODUCTION,
            token='EAAAlxjvASRtaL6M6BvfQv1_FyRqAyXH5R802IeuimZUBmeOGbhfgPvm9sMibtO1'
        )
        try:
            item_list = []
            item_response = client.catalog.list()
            for item in item_response:
                if item.type == 'ITEM' and hasattr(item, 'item_data') and item.item_data.name:
                    item_list.append(item.item_data.name.strip())
            item_list = sorted(list(set(item_list)))
            return Response({'items': item_list})
        except Exception as e:
            return Response({'error': str(e)}, status=500)