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

        self.expected = {
            'profile': 'https://techcrunch.com/author/jon-russell/',
            'website': 'https://www.crunchbase.com/person/jon-russell-2',
            'twitter': 'http://twitter.com/jonrussell',
            'linkedin': 'http://th.linkedin.com/in/jmarussell',
            'about': 'Jon Russell is an Asia-based writer for TechCrunch. Formerly he was an Asia editor for The Next Web.Jon Russell is passionate about the development of the internet, technology, and startups in Asia. He is based in Bangkok, Thailand. You can email him at jr@techcrunch.com or use his PGP key. Note: Jon owns a small amount of cryptocurrency. Enough to gain an understanding, not enough to change a life.',
            'avatar': 'https://crunchbase-production-res.cloudinary.com/image/upload/h_216,w_216,c_fit/v1444643798/hgdwby05oujsvjkj71jk.jpg'
        }


    @patch('requests.get')
    def test_techcrunch_extract_author_from_page(self, mock_get):
        """
        Tests if an author's information can be found at the article's page.
        """
        mock_get.return_value.content = get_file('techcrunch_author.html')

        parsed_article = parse_mocked('techcrunch_article.html', 'html')

        author = self.ws.extract_author_from_page(parsed_article)

        for key in author:
            self.assertEqual(author[key], self.expected[key])


    @patch('articles.scrapers.techcrunch.TechCrunch.parse')
    @patch('articles.scrapers.techcrunch.TechCrunch.extract_author_from_page')
    #@patch.object(articles.scrapers.techcrunch.TechCrunch, 'extract_author_from_page', fake_bar)
    def test_techcrunch_extract_author_wrong_url(self, mock_get1, mock_get2):
        """
        Tests if an author's information can be found by his/her name, assuming
        the generated author url was wrong and led to TechCrunch's home page.
        """

        # Extract_author should call extract_author_from_page, because the
        # provided page didn't had any information about the author. Let's
        # assume that `extract_author_from_page` is working correctly and mock
        # it.
        self.ws.article_page = ''
        parsed_author = parse_mocked('techcrunch_author.html', 'html')
        author = {
            'profile': 'https://techcrunch.com/author/jon-russell/',
            'flag': 'exit'
        }
        mock_get1.return_value = self.ws.extract_author(
            parsed_author, 'Jon Russel', author
        )
        mock_get2.return_value = None


        # We should be parsing techcrunch_author.html but the intention is to
        # trigger the problematic behavior.
        parsed_author = parse_mocked('techcrunch_article.html', 'html')
        author = self.ws.extract_author(parsed_author)

        for key in author:
            self.assertEqual(author[key], self.expected[key])


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