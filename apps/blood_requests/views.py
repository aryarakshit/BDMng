from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.timezone import now
from .models import BloodRequest
from .forms import BloodRequestForm
from apps.inventory.services import allocate_blood

class RequestListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BloodRequest
    template_name = 'requests/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20
    permission_required = 'blood_requests.view_bloodrequest'

    def get_queryset(self):
        status = self.request.GET.get('status', 'pending')
        return BloodRequest.objects.filter(status=status).select_related('requested_by').prefetch_related('allocated_units').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'pending')
        return context

class RequestCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BloodRequest
    form_class = BloodRequestForm
    template_name = 'requests/request_form.html'
    permission_required = 'blood_requests.add_bloodrequest'
    success_url = reverse_lazy('requests:list')

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        messages.success(self.request, "Blood request submitted successfully.")
        return super().form_valid(form)

class RequestDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BloodRequest
    template_name = 'requests/request_detail.html'
    context_object_name = 'blood_request'
    permission_required = 'blood_requests.view_bloodrequest'

class AllocateView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BloodRequest
    permission_required = 'blood_requests.change_bloodrequest'

    def get(self, request, *args, **kwargs):
        return redirect('requests:detail', pk=self.get_object().pk)

    def post(self, request, *args, **kwargs):
        blood_request = self.get_object()
        if blood_request.status != 'pending':
            messages.error(request, "This request has already been processed.")
            return redirect('requests:detail', pk=blood_request.pk)

        if allocate_blood(blood_request):
            messages.success(request, f"Successfully allocated blood for {blood_request.patient_name}.")
        else:
            messages.error(request, "Insufficient stock to fulfill this request.")

        return redirect('requests:detail', pk=blood_request.pk)

class RequestRejectView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BloodRequest
    permission_required = 'blood_requests.change_bloodrequest'

    def get(self, request, *args, **kwargs):
        return redirect('requests:detail', pk=self.get_object().pk)

    def post(self, request, *args, **kwargs):
        blood_request = self.get_object()
        if blood_request.status == 'pending':
            blood_request.status = 'rejected'
            blood_request.resolved_at = now()
            blood_request.save()
            messages.success(request, "Request rejected.")
        return redirect('requests:list')
