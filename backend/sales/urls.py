from django.urls import path
from sales.views import OrderStatsView

urlpatterns = [
    path('order-stats/', OrderStatsView.as_view(), name='order-stats'),
]