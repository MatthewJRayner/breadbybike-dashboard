from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django is working!")

# Create your views here.
class SquareStatsView(APIView):
    def get(self, request):
        # Mock data for now
        stats = {
            'total_sales': 1234.65,
            'order_count': 45,
            'average_order_value': 25.43
        }
        
        return Response(stats)

class ShopifyOrdersView(APIView):
    def get(self, request):
        return Response({"message": "Shopify orders endpoint"})