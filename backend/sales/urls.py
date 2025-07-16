from django.urls import path
from sales.views import OrderStatsView, TriggerCalculationsView, SquareCatalogItemsView, UpdateDailyStatsView, ShopifyOrdersView

urlpatterns = [
    path('order-stats/', OrderStatsView.as_view(), name='order-stats'),
    path('trigger-calculation/', TriggerCalculationsView.as_view(), name='trigger-calculation'),
    path('square-catalog-items/', SquareCatalogItemsView.as_view(), name='square-catalog-items'),
    path('update-daily-stats/', UpdateDailyStatsView.as_view(), name='update-daily-stats'),
    path('shopify-orders/', ShopifyOrdersView.as_view(), name='shopify-orders'),
]