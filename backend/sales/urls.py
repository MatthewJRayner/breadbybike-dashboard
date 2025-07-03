from django.urls import path
from sales.views import OrderStatsView, TriggerCalculationsView, SquareCatalogItemsView

urlpatterns = [
    path('order-stats/', OrderStatsView.as_view(), name='order-stats'),
    path('trigger-calculation/', TriggerCalculationsView.as_view(), name='trigger-calculation'),
    path('square-catalog-items/', SquareCatalogItemsView.as_view(), name='square-catalog-items')
]