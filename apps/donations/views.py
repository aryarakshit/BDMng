from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from datetime import timedelta, date
from .models import Donation
from .forms import DonationForm
from apps.donors.models import Donor
from apps.inventory.models import BloodUnit

class DonationListView(LoginRequiredMixin, ListView):
    model = Donation
    template_name = 'donations/donation_list.html'
    context_object_name = 'donations'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('donor', 'collected_by')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(donor__full_name__icontains=q) | Q(donor__phone__icontains=q))
        return qs.order_by('-donation_date')

class DonationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'donations/donation_form.html'
    permission_required = 'donations.add_donation'
    success_url = reverse_lazy('donations:list')

    def form_valid(self, form):
        with transaction.atomic():
            donor = Donor.objects.get(id=form.cleaned_data['donor_id'])
            form.instance.donor = donor
            form.instance.collected_by = self.request.user
            
            # Create Blood Unit
            unit = BloodUnit.objects.create(
                blood_group=donor.blood_group,
                units=form.instance.units_collected,
                collection_date=form.instance.donation_date,
                expiry_date=form.instance.donation_date + timedelta(days=42), # 42 days standard
                source_donor=donor,
                added_by=self.request.user
            )
            form.instance.blood_unit = unit
            
            response = super().form_valid(form)
            messages.success(self.request, f"Donation recorded for {donor.full_name}. Blood unit #{unit.id} added to inventory.")
            return response

class DonationDetailView(LoginRequiredMixin, DetailView):
    model = Donation
    template_name = 'donations/donation_detail.html'
    context_object_name = 'donation'

def donor_search_ajax(request):
    q = request.GET.get('q', '')
    if len(q) < 2:
        return JsonResponse({'results': []})
    
    donors = Donor.objects.filter(
        Q(full_name__icontains=q) | Q(phone__icontains=q),
        status='active'
    )[:10]
    
    results = []
    for d in donors:
        results.append({
            'id': d.id,
            'text': f"{d.full_name} ({d.blood_group}) - {d.phone}",
            'eligible': d.is_eligible,
            'blood_group': d.blood_group
        })
    
    return JsonResponse({'results': results})
