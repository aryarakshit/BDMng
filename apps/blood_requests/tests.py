from django.test import TestCase
from django.utils.timezone import now
from datetime import date, timedelta
from apps.donors.models import Donor
from apps.inventory.models import BloodUnit
from apps.blood_requests.models import BloodRequest
from apps.inventory.services import allocate_blood

class AllocationFlowTest(TestCase):
    def setUp(self):
        # 1. Create a Donor
        self.donor = Donor.objects.create(
            full_name="Test Donor",
            blood_group="O+",
            date_of_birth="1990-01-01",
            phone="1234567890"
        )
        
        # 2. Add Stock to Inventory
        self.unit = BloodUnit.objects.create(
            blood_group="O+",
            units=1,
            collection_date=date.today(),
            expiry_date=date.today() + timedelta(days=42),
            status='available',
            source_donor=self.donor
        )
        
        # 3. Create a Blood Request
        self.request = BloodRequest.objects.create(
            patient_name="Test Patient",
            hospital="Test Hospital",
            blood_group="O+",
            units_required=1,
            priority='urgent'
        )

    def test_allocation_success(self):
        """Test that blood allocation succeeds when stock is available."""
        success = allocate_blood(self.request)
        self.assertTrue(success)
        
        # Refresh from DB
        self.request.refresh_from_db()
        self.unit.refresh_from_db()
        
        self.assertEqual(self.request.status, 'approved')
        self.assertEqual(self.unit.status, 'reserved')
        self.assertIn(self.unit, self.request.allocated_units.all())

    def test_allocation_insufficient_stock(self):
        """Test that allocation fails when requested units exceed stock."""
        # Create a request for 5 units
        large_request = BloodRequest.objects.create(
            patient_name="Patient B",
            hospital="Hosp B",
            blood_group="O+",
            units_required=5
        )
        success = allocate_blood(large_request)
        self.assertFalse(success)
        self.assertEqual(large_request.status, 'pending')
