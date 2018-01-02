from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

class ViewTestCase(TestCase):
    """Test suite for the api endpoints."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()


    def test_api_retrieve_outlets(self):
        """Test the api is retrieving the outlets' list."""
        request = self.client.get(reverse('outlets'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_api_retrieve_categories(self):
        """Test the api is retrieving the categories' list."""
        request = self.client.get(reverse('categories'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_api_retrieve_authors(self):
        """Test the api is retrieving the authors' list."""
        request = self.client.get(reverse('authors'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_api_retrieve_articles(self):
        """Test the api is retrieving the articles' list."""
        request = self.client.get(reverse('articles'))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
