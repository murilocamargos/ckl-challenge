from django.test import TestCase

from articles.models import Outlet, Author, Category, Article
from articles.tests.utils import get_file, parse_mocked
from articles.scrapers.cheesecakelabs import CheesecakeLabs

from mock import patch
from lxml import html, etree
import dateutil.parser, json

class CheesecakeLabsScraperTestCase(TestCase):
    """This class defines the test suite for the CheesecakeLabs scraper."""

    def setUp(self):
        """Defines the test client and other test variables."""
        Outlet.objects.create(name = 'Cheesecake Labs')
        self.ws = CheesecakeLabs()


    def test_cheesecake_article_info(self):
        """Tests the correct data are extracted from an article's page."""
        parsed = parse_mocked('cheesecakelabs_article.html', 'html')

        results = self.ws.article_info(parsed)
        expct = ['title', 'categories', 'thumb', 'date', 'content', 'authors']

        self.assertEqual(list(results.keys()), expct)


    @patch('requests.get')
    def test_cheesecake_extract_articles(self, mock_get):
        """Tests if articles are being correctly extracted."""

        # This mock is used when some function tries to request from the web
        mock_get.return_value.content = get_file('cheesecakelabs_article.html')

        # Parses and extract information from Cheesecake Articles JSON feed
        article_feed = parse_mocked('cheesecakelabs_articles.json', 'json')
        articles_extracted = list(self.ws.extract_articles(article_feed))

        # This JSON mock has 20 articles
        self.assertEqual(len(articles_extracted), 20)

        # Check data integrity on the first article (mocking makes all equal)
        self.assertEqual(self.ws.check_data(articles_extracted[0]), None)


    def test_import_task(self):
        """Tries to import celery task function for CheesecakeLabs."""
        from articles.tasks import fetch_cheesecakelabs_articles