from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import BloodUnit
from .forms import BloodUnitForm

class InventoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BloodUnit
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'blood_units'
    paginate_by = 20
    permission_required = 'inventory.view_bloodunit'

    def get_queryset(self):
        qs = BloodUnit.objects.select_related('source_donor', 'added_by').all()
        blood_group = self.request.GET.get('blood_group')
        status = self.request.GET.get('status')
        if blood_group:
            qs = qs.filter(blood_group=blood_group)
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('expiry_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blood_group_choices'] = BloodUnit.BLOOD_GROUP_CHOICES
        context['status_choices'] = BloodUnit.STATUS_CHOICES
        context['current_blood_group'] = self.request.GET.get('blood_group', '')
        context['current_status'] = self.request.GET.get('status', '')
        return context

class InventoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BloodUnit
    form_class = BloodUnitForm
    template_name = 'inventory/inventory_form.html'
    permission_required = 'inventory.add_bloodunit'
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, "Blood unit added to inventory.")
        return super().form_valid(form)

class InventoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BloodUnit
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'unit'
    permission_required = 'inventory.view_bloodunit'

class InventoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BloodUnit
    form_class = BloodUnitForm
    template_name = 'inventory/inventory_form.html'
    permission_required = 'inventory.change_bloodunit'
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        messages.success(self.request, "Blood unit updated successfully.")
        return super().form_valid(form)

class InventoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BloodUnit
    template_name = 'inventory/inventory_confirm_delete.html'
    permission_required = 'inventory.delete_bloodunit'
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        messages.success(self.request, "Blood unit deleted.")
        return super().form_valid(form)
