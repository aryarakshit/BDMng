from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Donor
from .forms import DonorForm

class DonorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Donor
    template_name = 'donors/donor_list.html'
    context_object_name = 'donors'
    paginate_by = 20
    permission_required = 'donors.view_donor'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        bg = self.request.GET.get('blood_group')
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(phone__icontains=q))
        if bg:
            qs = qs.filter(blood_group=bg)
        return qs

class DonorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donors/donor_form.html'
    permission_required = 'donors.add_donor'
    success_url = reverse_lazy('donors:list')

    def form_valid(self, form):
        messages.success(self.request, "Donor registered successfully.")
        return super().form_valid(form)

class DonorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Donor
    form_class = DonorForm
    template_name = 'donors/donor_form.html'
    permission_required = 'donors.change_donor'
    success_url = reverse_lazy('donors:list')

    def form_valid(self, form):
        messages.success(self.request, "Donor profile updated successfully.")
        return super().form_valid(form)

class DonorDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Donor
    template_name = 'donors/donor_detail.html'
    context_object_name = 'donor'
    permission_required = 'donors.view_donor'

class DonorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Donor
    template_name = 'donors/donor_confirm_delete.html'
    permission_required = 'donors.delete_donor'
    success_url = reverse_lazy('donors:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Donor deleted successfully.")
        return super().delete(request, *args, **kwargs)
