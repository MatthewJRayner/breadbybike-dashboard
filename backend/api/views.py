from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django is working!")

# Create your views here.
class SquareStatsView(APIView):
    def get(self, request):
        return Response({"message": "Square stats endpoint"})

class ShopifyOrdersView(APIView):
    def get(self, request):
        return Response({"message": "Shopify orders endpoint"})