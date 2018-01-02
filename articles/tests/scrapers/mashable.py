from mock import patch

from django.test import TestCase

from articles.scrapers.mashable import Mashable
from articles.tests.utils import get_file, parse_mocked
from articles.models import Outlet

class MashableScraperTestCase(TestCase):
    """This class defines the test suite for the Mashable scraper."""

    def setUp(self):
        """Defines the test client and other test variables."""
        Outlet.objects.create(name='Mashable')
        self.scraper = Mashable()

        self.author = {
            'twitter': 'https://twitter.com/http://t.co/czrMuR82PU',
            'website': 'https://plus.google.com/102055917606956087205',
            'about': "Adam Rosenberg is a Senior Games Reporter for Mashable, where he plays all the games. Every single one. From AAA blockbusters to indie darlings to mobile favorites and browser-based oddities, he consumes as much as he can, whenever he can.Adam brings more than a decade of experience working in the space to the Mashable Games team. He previously headed up all games coverage at Digital Trends, and prior to that was a long-time, full-time freelancer, writing for a diverse lineup of outlets that includes Rolling Stone, MTV, G4, Joystiq, IGN, Official Xbox Magazine, EGM, 1UP, UGO and others.Born and raised in the beautiful suburbs of New York, Adam has spent his life in and around the city. He's a New York University graduate with a double major in Journalism and Cinema Studios. He's also a certified audio engineer. Currently, Adam resides in Crown Heights with his dog and his partner's two cats. He's a lover of fine food, adorable animals, video games, all things geeky and shiny gadgets.",
            'profile': 'http://mashable.com/author/adam-rosenberg/',
            'avatar': 'https://i.amz.mshcdn.com/7pSDrJGVpU1vRcxw5phAdPru3os=/200x200/2016%2F09%2F16%2F63%2Fhttpsd2mhye01h4nj2n.cloudfront.netmediaZgkyMDE1LzA2.c97cf.jpg'
        }


    def test_mash_author_page_unsetted(self):
        """Tests if author's url page is being correctly generated."""
        url = self.scraper.get_authors_page('Jon Snow')
        self.assertEqual('http://mashable.com/author/jon-snow', url)


    def test_mash_author_page_setted(self):
        """Tests if author's url page is being correctly generated."""
        self.scraper.author_url = 'completly-different-url'

        url = self.scraper.get_authors_page('Jon Snow')
        self.assertEqual('completly-different-url', url)


    @patch('requests.get')
    def test_mashable_get_author(self, mock_get):
        """Tests if an author's information can be found by his/her name."""
        mock_get.return_value.content = get_file('mashable_author.html')

        result = self.scraper.get_author('Adam Rosenberg')

        self.assertEqual(result['name'], 'Adam Rosenberg')


    def test_mashable_extract_author(self):
        """Tests if an author's information can be extracted from his page."""
        parsed = parse_mocked('mashable_author.html', 'html')

        result = self.scraper.extract_author(parsed)

        for key in result:
            self.assertEqual(result[key], self.author[key])


    @patch('articles.scrapers.scraper.WebScraper.get_author')
    @patch('requests.get')
    def test_mashable_extract_articles(self, mock_get1, mock_get2):
        """Tests if an article list can be extracted from twitter feed."""

        # This mock is used when some function tries to request from the web.
        # The extract_articles method tries to do this twice, one for gathering
        # article's content from the article's page and another for the author.
        mock_get1.return_value.content = get_file('mashable_article.html')
        mock_get2.return_value = self.author

        # Parses and extract information from Mashable Articles Twitter feed
        article_feed = parse_mocked('mashable_twitter', 'twitter')
        articles_extracted = list(self.scraper.extract_articles(article_feed))

        # This JSON mock has 20 articles
        self.assertEqual(len(articles_extracted), 19)

        # Check data integrity on the first article (mocking makes all equal)
        self.assertEqual(self.scraper.check_data(articles_extracted[0]), None)
