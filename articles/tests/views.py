from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Author, Outlet, Category, Article

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
            'name': 'Linus Torvalds',
            'slug': 'linus-torvalds'
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
            'slug': 'donald-knuth'
        }

        request = self.client.post(reverse('author-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)



class CategoryViewTestCase(TestCase):
    """Test suite for the api endpoints related to categories."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()

        self.user = User.objects.create(username = 'nerd', is_staff = True)
        self.category = Category.objects.create(name = 'Linux')

        self.epoint = reverse('category', kwargs = {'pk': 1})

    def test_api_delete_category_unlogged(self):
        """Test if an unlogged user can delete a category."""
        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_add_category_unlogged(self):
        """Test if an unlogged user can add a category."""
        data = {
            'name': 'Windows',
            'slug': 'windows'
        }

        request = self.client.post(reverse('category-create'), data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_update_category_unlogged(self):
        """Test if an unlogged user can delete a category."""
        data = {'name': 'Nginx'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_retrieve_category_unlogged(self):
        """Test if an unlogged user can retrieve a category."""
        request = self.client.get(self.epoint)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_api_update_category_logged(self):
        """Test if an logged user can delete a category."""
        self.client.force_authenticate(user = self.user)

        data = {'name': 'AWS'}

        request = self.client.patch(self.epoint, data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_api_delete_category_logged(self):
        """Test if an logged user can delete a category."""
        self.client.force_authenticate(user = self.user)

        request = self.client.delete(self.epoint)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_add_category_logged(self):
        """Test if an logged user can add a category."""
        self.client.force_authenticate(user = self.user)

        data = {
            'name': 'Redis',
            'slug': 'redis'
        }

        request = self.client.post(reverse('category-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)




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
            'name': 'Marshable',
            'slug': 'marshable',
            'website': 'marshable.com',
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
            'slug': 'siliconbeat',
            'website': 'siliconbeat.com',
        }

        request = self.client.post(reverse('outlet-create'), data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)




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