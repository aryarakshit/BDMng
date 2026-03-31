from django.urls import path
from .views import DonorListView, DonorCreateView, DonorDetailView, DonorUpdateView, DonorDeleteView

app_name = 'donors'

urlpatterns = [
    path('',              DonorListView.as_view(),   name='list'),
    path('add/',          DonorCreateView.as_view(), name='create'),
    path('<int:pk>/',     DonorDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', DonorUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DonorDeleteView.as_view(), name='delete'),
]
