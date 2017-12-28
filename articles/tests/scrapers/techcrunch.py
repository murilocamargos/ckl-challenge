from django.test import TestCase

from articles.scrapers.techcrunch import TechCrunch
from articles.tests.utils import get_file, parse_mocked
from articles.models import Author, Outlet

from mock import patch
from lxml import html, etree
import os, json

class TechCrunchScraperTestCase(TestCase):
    """This class defines the test suite for the TechCrunch scraper."""

    def setUp(self):
        """Defines the test client and other test variables."""
        Outlet.objects.create(name = 'TechCrunch')
        self.ws = TechCrunch()

    def test_techcrunch_extract_twitter_single(self):
        """Tests twitter extraction for single author articles."""
        parsed = parse_mocked('techcrunch_single_author.html', 'html')
        
        twitter = self.ws.extract_twitter(parsed)
        self.assertEqual(twitter, 'https://twitter.com/jglasner')


    def test_techcrunch_extract_twitter_multiple(self):
        """Tests twitter extraction for multiple author articles."""
        parsed = parse_mocked('techcrunch_multiple_authors.html', 'html')

        twitter_1 = self.ws.extract_twitter(parsed, 'Anthony Ha')
        self.assertEqual(twitter_1, 'https://twitter.com/anthonyha')

        twitter_2 = self.ws.extract_twitter(parsed, 'Darrell Etherington')
        self.assertEqual(twitter_2, 'https://twitter.com/etherington')


    def test_techcrunch_get_authors_page(self):
        """Tests if author's url page is being correctly generated."""
        url = self.ws.get_authors_page('Jon Snow')
        self.assertEqual('http://techcrunch.com/author/jon-snow', url)


    @patch('requests.get')
    def test_techcrunch_get_author(self, mock_get):
        """Tests if an author's information can be found by his/her name."""
        mock_get.return_value.content = get_file('techcrunch_author.html')

        result = self.ws.get_author('Jon Russell')

        self.assertEqual(result['name'], 'Jon Russell')


    def test_techcrunch_extract_author(self):
        """Tests if an author's information can be extracted from his page."""
        parsed = parse_mocked('techcrunch_author.html', 'html')

        result = self.ws.extract_author(parsed)
        result = list(result.keys())

        expected = ['twitter', 'linkedin', 'about', 'profile', 'avatar']

        self.assertEqual(result, expected)


    @patch('requests.get')
    def test_techcrunch_extract_articles(self, mock_get):
        """Tests if an article list can be extracted from xml feed."""

        # This mock is used when some function tries to request from the web
        mock_get.return_value.content = get_file('techcrunch_author.html')

        # Parses and extract information from TechCrunch Articles XML feed
        article_feed = parse_mocked('techcrunch_articles.xml', 'xml')
        articles_extracted = list(self.ws.extract_articles(article_feed))

        # This JSON mock has 20 articles
        self.assertEqual(len(articles_extracted), 20)

        # Check data integrity on the first article (mocking makes all equal)
        self.assertEqual(self.ws.check_data(articles_extracted[0]), None)