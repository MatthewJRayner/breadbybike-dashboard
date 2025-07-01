from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sales.models import OrderStats
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

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