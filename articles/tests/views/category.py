from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Category


class CategoryViewTestCase(TestCase):
    """Test suite for the api endpoints related to categories."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        self.user = User.objects.create(username='nerd', is_staff=True)
        self.category = Category.objects.create(name='Linux')

        self.epoint = reverse('category', kwargs={'pk': 1})


    def test_delete_category_unlogged(self):
        """Test if an unlogged user can delete a category."""
        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_add_category_unlogged(self):
        """Test if an unlogged user can add a category."""
        data = {
            'name': 'Windows',
            'slug': 'windows'
        }

        request = self.client.post(reverse('category-create'), data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_category_unlogged(self):
        """Test if an unlogged user can delete a category."""
        data = {'name': 'Nginx'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve_category_unlogged(self):
        """Test if an unlogged user can retrieve a category."""
        request = self.client.get(self.epoint)

        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_update_category_logged(self):
        """Test if an logged user can delete a category."""
        self.client.force_authenticate(user=self.user)

        data = {'name': 'AWS'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_delete_category_logged(self):
        """Test if an logged user can delete a category."""
        self.client.force_authenticate(user=self.user)

        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)


    def test_add_category_logged(self):
        """Test if an logged user can add a category."""
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Redis',
            'slug': 'redis'
        }

        request = self.client.post(reverse('category-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
