from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Author, Outlet, Category, Article


class ArticleViewTestCase(TestCase):
    """Test suite for the api endpoints related to articles."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        self.user = User.objects.create(username = 'nerd', is_staff = True)

        self.outlet = Outlet.objects.create(name = 'TechCrunch')
        self.article = Article.objects.create(title = 'Article',
            date = str(timezone.now()), url = 'Link', content = 'Article',
            outlet_id = self.outlet.id),

        self.epoint = reverse('article', kwargs = {'pk': 1})


    def test_api_delete_article_unlogged(self):
        """Test if an unlogged user can delete an article."""
        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_api_add_article_unlogged(self):
        """Test if an unlogged user can add an article."""
        data = {
            'title': 'Article\'s title',
            'date': str(timezone.now()),
            'url': 'https://outlet.com/article',
            'content': 'Article\'s content',
            'outlet': self.outlet.id,
        }

        request = self.client.post(reverse('article-create'), data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_api_update_article_unlogged(self):
        """Test if an unlogged user can delete an article."""
        data = {'title': 'Changed title'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_api_retrieve_article_unlogged(self):
        """Test if an unlogged user can retrieve an article."""
        request = self.client.get(self.epoint)

        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_api_update_article_logged(self):
        """Test if an logged user can delete an article."""
        self.client.force_authenticate(user = self.user)

        data = {'name': 'Changed title'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)


    def test_api_delete_article_logged(self):
        """Test if an logged user can delete an article."""
        self.client.force_authenticate(user = self.user)

        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)


    def test_api_add_article_logged(self):
        """Test if an logged user can add an article."""
        self.client.force_authenticate(user = self.user)

        data = {
            'title': 'Article\'s title',
            'date': str(timezone.now()),
            'url': 'https://outlet.com/article',
            'content': 'Article\'s content',
            'outlet': self.outlet.id,
        }

        request = self.client.post(reverse('article-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)