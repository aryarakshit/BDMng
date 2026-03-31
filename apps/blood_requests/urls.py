from django.urls import path
from .views import RequestListView, RequestCreateView, RequestDetailView, AllocateView, RequestRejectView

app_name = 'requests'

urlpatterns = [
    path('',              RequestListView.as_view(),   name='list'),
    path('add/',          RequestCreateView.as_view(), name='create'),
    path('<int:pk>/',     RequestDetailView.as_view(), name='detail'),
    path('<int:pk>/allocate/', AllocateView.as_view(),  name='allocate'),
    path('<int:pk>/reject/',   RequestRejectView.as_view(), name='reject'),
]
