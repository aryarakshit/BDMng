from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.donors.models import Donor
from apps.inventory.models import BloodUnit
from apps.blood_requests.models import BloodRequest
from apps.donations.models import Donation
from django.db.models import Sum
from datetime import date

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_donors'] = Donor.objects.count()
        context['available_units'] = BloodUnit.objects.filter(status='available').aggregate(total=Sum('units'))['total'] or 0
        context['pending_requests'] = BloodRequest.objects.filter(status='pending').count()
        context['todays_donations'] = Donation.objects.filter(donation_date=date.today()).count()
        context['recent_donations'] = Donation.objects.select_related('donor').order_by('-donation_date')[:5]
        return context
