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

        expected = {
            'name': 'Jon Russell',
            'twitter': 'http://twitter.com/jonrussell',
            'linkedin': 'http://th.linkedin.com/in/jmarussell',
            'profile': 'https://www.crunchbase.com/person/jon-russell-2',
            'avatar': 'https://crunchbase-production-res.cloudinary.com/image/upload/h_216,w_216,c_fit/v1444643798/hgdwby05oujsvjkj71jk.jpg',
            'about': 'Jon Russell is an Asia-based writer for TechCrunch. Formerly he was an Asia editor for The Next Web.Jon Russell is passionate about the development of the internet, technology, and startups in Asia. He is based in Bangkok, Thailand. You can email him at jr@techcrunch.com or use his PGP key. Note: Jon owns a small amount of cryptocurrency. Enough to gain an understanding, not enough to change a life.'
        }

        for key in expected:
            self.assertEqual(result[key], expected[key])


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


    def test_import_task(self):
        """Tries to import celery task function for TechCrunch."""
        from articles.tasks import fetch_techcrunch_articles