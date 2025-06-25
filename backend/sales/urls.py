from django.urls import path
from . import views

urlpatterns = [
    path('square/stats/', views.SquareStatsView.as_view(), name='square_stats'),
    path('shopify/orders/', views.ShopifyOrdersView.as_view(), name='shopify_orders'),
]