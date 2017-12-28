from django.test import TestCase

from articles.scrapers.engadget import Engadget
from articles.tests.utils import get_file, parse_mocked
from articles.models import Author, Outlet

from mock import patch
from lxml import html, etree
import os, json

class EngadgetScraperTestCase(TestCase):
    """This class defines the test suite for the Engadget scraper."""

    def setUp(self):
        """Defines the test client and other test variables."""
        Outlet.objects.create(name = 'Engadget')
        self.ws = Engadget()


    def test_engadget_extract_twitter_single(self):
        """Tests twitter extraction for single author articles."""
        parsed = parse_mocked('engadget_single_author.html', 'html')

        twitter = self.ws.extract_twitter(parsed)
        self.assertEqual(twitter, 'https://twitter.com/eightiethmnt')


    def test_engadget_get_authors_page(self):
        """Tests if author's url page is being correctly generated."""
        url = self.ws.get_authors_page('Jon Snow')
        self.assertEqual('http://www.engadget.com/about/editors/jon-snow', url)


    @patch('requests.get')
    def test_engadget_get_author(self, mock_get):
        """Tests if an author's information can be found by his/her name."""
        mock_get.return_value.content = get_file('engadget_author.html')

        result = self.ws.get_author('Christopher Trout')

        expected = {
            'name': 'Christopher Trout',
            'twitter': 'https://twitter.com/@Mr_Trout',
            'profile': 'https://www.engadget.com/about/editors/christopher-trout/',
            'avatar': 'https://s.blogcdn.com/www.engadget.com/media/2017/04/christophertrouteditorinchiefengsquare.jpg',
            'about': 'Before starting at Engadget, Christopher worked in a series of jobs that would make your mother blush. He&#8217;s since acted as executive editor of the award-winning digital magazine&#160;Distro as well as Engadget.com. His column&#160;&#8220;Computer Love&#8221; explores the weird world of human sexuality in the 21st century. When he&#8217;s not writing about sex robots and VR porn, you can find him at the bottom of a martini glass.'
        }

        for key in expected:
            self.assertEqual(result[key], expected[key])


    @patch('requests.get')
    def test_engadget_extract_articles(self, mock_get):
        """Tests if an article list can be extracted from xml feed."""

        # This mock is used when some function tries to request from the web
        mock_get.return_value.content = get_file('engadget_author.html')

        # Parses and extract information from Engadget Articles XML feed
        article_feed = parse_mocked('engadget_articles.xml', 'xml')
        articles_extracted = list(self.ws.extract_articles(article_feed))

        # This JSON mock has 20 articles
        self.assertEqual(len(articles_extracted), 25)

        # Check data integrity on the first article (mocking makes all equal)
        self.assertEqual(self.ws.check_data(articles_extracted[0]), None)


    def test_import_task(self):
        """Tries to import celery task function for Engadget."""
        from articles.tasks import fetch_engadget_articles