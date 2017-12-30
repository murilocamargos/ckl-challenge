from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Author


class AuthorViewTestCase(TestCase):
    """Test suite for the api endpoints related to authors."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        self.user = User.objects.create(username = 'nerd', is_staff = True)
        self.author = Author.objects.create(name = 'Dennis Ritchie')

        self.epoint = reverse('author', kwargs = {'pk': 1})

    
    def test_api_delete_author_unlogged(self):
        """Test if an unlogged user can delete an author."""
        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_api_add_author_unlogged(self):
        """Test if an unlogged user can add an author."""
        data = {
            'name': 'Linus Torvalds'
        }

        request = self.client.post(reverse('author-create'), data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_api_update_author_unlogged(self):
        """Test if an unlogged user can delete an author."""
        data = {'name': 'Ken Thompson'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_api_retrieve_author_unlogged(self):
        """Test if an unlogged user can retrieve an author."""
        request = self.client.get(self.epoint)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    
    def test_api_update_author_logged(self):
        """Test if an logged user can delete an author."""
        self.client.force_authenticate(user = self.user)

        data = {'name': 'Ken Thompson'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    
    def test_api_delete_author_logged(self):
        """Test if an logged user can delete an author."""
        self.client.force_authenticate(user = self.user)

        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_api_add_author_logged(self):
        """Test if an logged user can add an author."""
        self.client.force_authenticate(user = self.user)

        data = {
            'name': 'Donald Knuth',
        }

        request = self.client.post(reverse('author-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)