from django.test import TestCase

from articles.scrapers.mashable import Mashable
from articles.tests.utils import get_file, parse_mocked
from articles.models import Author, Outlet

from mock import patch
from lxml import html, etree
import os, json

class MashableScraperTestCase(TestCase):
    """This class defines the test suite for the Mashable scraper."""

    def setUp(self):
        """Defines the test client and other test variables."""
        Outlet.objects.create(name = 'Mashable')
        self.ws = Mashable()


    def test_mashable_get_authors_page_without_setting(self):
        """Tests if author's url page is being correctly generated."""
        url = self.ws.get_authors_page('Jon Snow')
        self.assertEqual('http://mashable.com/author/jon-snow', url)


    def test_mashable_get_authors_page_with_setting(self):
        """Tests if author's url page is being correctly generated."""
        self.ws.author_url = 'completly-different-url'

        url = self.ws.get_authors_page('Jon Snow')
        self.assertEqual('completly-different-url', url)


    @patch('requests.get')
    def test_mashable_get_author(self, mock_get):
        """Tests if an author's information can be found by his/her name."""
        mock_get.return_value.content = get_file('mashable_author.html')

        result = self.ws.get_author('Adam Rosenberg')

        self.assertEqual(result['name'], 'Adam Rosenberg')


    def test_mashable_extract_author(self):
        """Tests if an author's information can be extracted from his page."""
        parsed = parse_mocked('mashable_author.html', 'html')

        result = self.ws.extract_author(parsed)
        result = list(result.keys())

        expected = ['twitter', 'website', 'about', 'profile', 'avatar']

        self.assertEqual(result, expected)


    @patch('requests.get')
    @patch('requests.get')
    def test_mashable_extract_articles(self, mock_get1, mock_get2):
        """Tests if an article list can be extracted from twitter feed."""

        # This mock is used when some function tries to request from the web.
        # The extract_articles method tries to do this twice, one for gathering
        # article's content from the article's page and another for the author.
        mock_get1.return_value.content = get_file('mashable_author.html')
        mock_get2.return_value.content = get_file('mashable_article.html')

        # Parses and extract information from TechCrunch Articles XML feed
        article_feed = parse_mocked('mashable_twitter', 'twitter')
        articles_extracted = list(self.ws.extract_articles(article_feed))

        # This JSON mock has 20 articles
        self.assertEqual(len(articles_extracted), 19)

        # Check data integrity on the first article (mocking makes all equal)
        self.assertEqual(self.ws.check_data(articles_extracted[0]), None)