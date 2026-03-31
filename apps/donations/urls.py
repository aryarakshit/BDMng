from django.urls import path
from .views import DonationListView, DonationCreateView, DonationDetailView, donor_search_ajax

app_name = 'donations'

urlpatterns = [
    path('',              DonationListView.as_view(),   name='list'),
    path('add/',          DonationCreateView.as_view(), name='create'),
    path('<int:pk>/',     DonationDetailView.as_view(), name='detail'),
    path('search-donor/', donor_search_ajax,            name='search_donor'),
]
