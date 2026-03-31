from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.ReportsDashboardView.as_view(), name='dashboard'),
    
    # AJAX endpoints
    path('api/donation-trend/', views.DonationTrendAPI.as_view(), name='api-donation-trend'),
    path('api/blood-group-distribution/', views.BloodGroupDistributionAPI.as_view(), name='api-blood-group-distribution'),
    path('api/kpi-summary/', views.KPISummaryAPI.as_view(), name='api-kpi-summary'),
    
    # Export endpoints
    path('export/pdf/', views.ExportPDFView.as_view(), name='export-pdf'),
    path('export/excel/', views.ExportExcelView.as_view(), name='export-excel'),
]
