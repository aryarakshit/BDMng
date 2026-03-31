from datetime import date, timedelta
from django.db import transaction
from django.utils.timezone import now
from .models import BloodUnit

def allocate_blood(request_obj):
    """
    Allocate available blood units to a request.
    Returns True if allocation succeeded, False if insufficient stock.
    """
    units = BloodUnit.objects.filter(
        blood_group=request_obj.blood_group,
        status='available',
        expiry_date__gte=date.today()
    ).order_by('expiry_date')[:request_obj.units_required]  # FEFO — First Expiry First Out

    if units.count() < request_obj.units_required:
        return False

    with transaction.atomic():
        # Using a loop to update individual units or a queryset update if applicable
        # The update() method is more efficient
        units_ids = list(units.values_list('id', flat=True))
        BloodUnit.objects.filter(id__in=units_ids).update(status='reserved')
        
        request_obj.allocated_units.set(units_ids)
        request_obj.status = 'approved'
        request_obj.resolved_at = now()
        request_obj.save()
    return True


def check_expiring_stock(days=7):
    """Return blood units expiring within `days` days."""
    threshold = date.today() + timedelta(days=days)
    return BloodUnit.objects.filter(
        status='available',
        expiry_date__lte=threshold,
        expiry_date__gte=date.today()
    )
