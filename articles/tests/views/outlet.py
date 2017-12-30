from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Outlet

class OutletViewTestCase(TestCase):
    """Test suite for the api endpoints related to outlets."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        self.user = User.objects.create(username = 'nerd', is_staff = True)
        self.outlet = Outlet.objects.create(name = 'TechCrunch')

        self.epoint = reverse('outlet', kwargs = {'pk': 1})

    
    def test_api_delete_outlet_unlogged(self):
        """Test if an unlogged user can delete an outlet."""
        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_api_add_outlet_unlogged(self):
        """Test if an unlogged user can add an outlet."""
        data = {
            'name': 'Mashable',
            'website': 'mashable.com',
        }

        request = self.client.post(reverse('outlet-create'), data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_api_update_outlet_unlogged(self):
        """Test if an unlogged user can delete an outlet."""
        data = {'name': 'Gizmodo'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_api_retrieve_outlet_unlogged(self):
        """Test if an unlogged user can retrieve an outlet."""
        request = self.client.get(self.epoint)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    
    def test_api_update_outlet_logged(self):
        """Test if an logged user can delete an outlet."""
        self.client.force_authenticate(user = self.user)

        data = {'name': 'Engadget'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    
    def test_api_delete_outlet_logged(self):
        """Test if an logged user can delete an outlet."""
        self.client.force_authenticate(user = self.user)

        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_api_add_outlet_logged(self):
        """Test if an logged user can add an outlet."""
        self.client.force_authenticate(user = self.user)

        data = {
            'name': 'SiliconBeat',
            'website': 'siliconbeat.com',
        }

        request = self.client.post(reverse('outlet-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
