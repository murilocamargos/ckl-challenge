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


    def test_outlet_default_slug(self):
        """Tests if the outlet's name is slugified by default."""
        self.outlet.save()
        self.assertEqual(self.outlet.slug, 'tech-crunch')


    def test_outlet_defined_slug(self):
        """Tests if the model accepts a user defined slug."""
        self.outlet.slug = 'tcrunch'
        self.outlet.save()
        self.assertEqual(self.outlet.slug, 'tcrunch')