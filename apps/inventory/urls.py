from django.urls import path

from .views import (
    InventoryListView, InventoryCreateView, InventoryDetailView,
    InventoryUpdateView, InventoryDeleteView,
)

app_name = 'inventory'

urlpatterns = [
    path('', InventoryListView.as_view(), name='list'),
    path('add/', InventoryCreateView.as_view(), name='create'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', InventoryUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', InventoryDeleteView.as_view(), name='delete'),
]
