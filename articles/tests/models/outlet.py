from django.test import TestCase
from articles.models import Outlet

class OutletModelTestCase(TestCase):
    """This class defines the test suite for the Outlet model."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.name = "Tech Crunch"
        self.outlet = Outlet(name = self.name)


    def test_outlet_can_create(self):
        """Tests if the outlet model can create an outlet."""
        old_count = Outlet.objects.count()
        self.outlet.save()
        new_count = Outlet.objects.count()
        self.assertNotEqual(old_count, new_count)


    def test_outlet_string_representation(self):
        """Tests if the outlet is correctly represented."""
        self.assertEqual(str(self.outlet), self.name)


    def test_outlet_can_update_patched(self):
        """Tests if an outlet can be updated or patched."""
        self.outlet.save()

        self.outlet.website = 'tcrunch.com'
        self.outlet.save()

        search = Outlet.objects.filter(website = 'tcrunch.com').count()
        self.assertEqual(search, 1)


    def test_outlet_can_delete(self):
        """Tests if an outlet can be hard deleted."""
        self.outlet.save()
        self.outlet.delete()
        search = Outlet.objects.filter(name = self.name)
        self.assertEqual(search.count(), 1)
        self.assertEqual(search.first().active, False)