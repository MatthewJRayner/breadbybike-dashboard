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
    """

    def post(self, request):
        """
        Handle POST request to calculate and save item statistics.

        Args:
            request: HTTP request object containing 'location' and 'item_name' in data.

        Returns:
            Response: JSON response with success message or error details.
        """
        # Extract and validate input
        location = request.data.get('location')
        item_name = request.data.get('item_name')  # Match frontend key

        if not location or not item_name:
            return Response({'error': 'Location and item name are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(location, str) or not isinstance(item_name, str):
            return Response({'error': 'Location and item name must be strings'}, status=status.HTTP_400_BAD_REQUEST)

        item_key = f'{location}_items_{item_name}'

        try:
            # Initialize stats from config or default
            stats = copy.deepcopy(items_stats)

            # Query data with consistent field names (adjust if different)
            order_lines = OrderLine.objects.filter(name=item_name)  # Limit to 1000 records for performance
            daily_orders = DailyOrderSnapshot.objects.filter(name=item_name)  # Limit to 1000 records

            if not order_lines.exists() and not daily_orders.exists():
                return Response({'error': f'No data found for item {item_name}'}, status=status.HTTP_404_NOT_FOUND)

            # Perform calculations
            if order_lines.exists():
                calc_items_stats(stats, OrderLine.objects.filter(name=item_name))
            if daily_orders.exists():
                calc_daily_stats_items(stats, DailyOrderSnapshot.objects.filter(name=item_name))
            
            

            # Serialize stats
            serialized_stats = convert_to_serializable(stats)

            # Update or create stats record
            OrderStats.objects.update_or_create(
                location=item_key,
                defaults={'stats_json': serialized_stats}
            )
            
            return Response({'message': f'Stats calculated for {item_key}'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response({'error': f'Database error: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': f'Validation error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SquareCatalogItemsView(APIView):
    def get(self, request):
        client = Square(
            environment=SquareEnvironment.PRODUCTION,
            token='EAAAlxjvASRtaL6M6BvfQv1_FyRqAyXH5R802IeuimZUBmeOGbhfgPvm9sMibtO1'
        )
        try:
            item_list = []
            item_response = client.catalog.list()
            for item in item_response:
                if item.type == 'ITEM':
                    item_list.append(item.item_data.name)
            return Response({'items': item_list})
        except Exception as e:
            return Response({'error': str(e)}, status=500)