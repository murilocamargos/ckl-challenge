from django.test import TestCase
from lxml import html, etree
import os
from articles.scrapers.scraper import WebScraper
from articles.scrapers.techcrunch import TechCrunch
from articles.models import Author, Outlet

def parse_html(file_name):
    """Helper function to parse html files for testing."""
    file_path = os.path.join(os.path.dirname(__file__), 'files/' + file_name)
    return html.parse(file_path)

class WebScrapperTestCase(TestCase):
    """This class defines the test suite for the web scrapers."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.ws = WebScraper()

    def test_webscraper_download(self):
        """Tests if download method is returning a lxml tree (parsed file)."""

        host = 'http://www.google.com'

        xml_tree = self.ws.download(host + '/sitemap.xml', 'xml')
        self.assertNotEqual(xml_tree, None)

        html_tree = self.ws.download(host + '/', 'html')
        self.assertNotEqual(html_tree, None)

    def test_webscraper_classify_links(self):
        """Tests links social network links classification."""
        links = [
            'http://www.facebook.com/matthew.panzarino',
            'http://twitter.com/Panzer',
            'https://www.linkedin.com/in/matthewpanzarino',
            '/author/matthew-panzarino/feed/',
            'http://th.linkedin.com/in/jmarussell'
        ]

        results = self.ws.classify_links(links)
        
        self.assertEqual(results, [
            ('facebook', 'http://www.facebook.com/matthew.panzarino'),
            ('twitter', 'http://twitter.com/Panzer'),
            ('linkedin', 'https://www.linkedin.com/in/matthewpanzarino'),
            ('linkedin', 'http://th.linkedin.com/in/jmarussell')
        ])

    def test_webscraper_html_to_string(self):
        """Test if html conversion of a lxml item is working correctly."""

        # Loads and parse html exemplo file
        file = os.path.join(os.path.dirname(__file__), 'files/author.html')
        tree = html.parse(file)

        # Search for h2 tags inside anything with id equals to `latest`
        find_item = tree.xpath('//*[@id="latest"]/h2')
        result = ''
        if find_item:
            result = self.ws.html_to_string(find_item[0]).strip()

        expected = '<h2 class="section-title">Latest from Jon Russell</h2>'

        self.assertEqual(result, expected)

class TechCrunchScraperTestCase(TestCase):
    """This class defines the test suite for the TechCrunch scraper."""

    def setUp(self):
        """Defines the test client and other test variables."""
        Outlet.objects.create(name = 'TechCrunch')
        self.ws = TechCrunch()

        file = os.path.join(os.path.dirname(__file__), 'files/articles.xml')
        self.articles_tree = etree.parse(file)

    def test_techcrunch_extract_twitter_single(self):
        """Tests twitter extraction for single author articles."""
        parsed = parse_html('article_single_author.html')
        
        twitter = self.ws.extract_twitter(parsed)
        self.assertEqual(twitter, 'https://twitter.com/jglasner')

    def test_techcrunch_extract_twitter_multiple(self):
        """Tests twitter extraction for multiple author articles."""
        parsed = parse_html('article_multiple_authors.html')

        twitter_1 = self.ws.extract_twitter(parsed, 'Anthony Ha')
        self.assertEqual(twitter_1, 'https://twitter.com/anthonyha')

        twitter_2 = self.ws.extract_twitter(parsed, 'Darrell Etherington')
        self.assertEqual(twitter_2, 'https://twitter.com/etherington')

    def test_techcrunch_get_authors_page(self):
        """Tests if author's url page is being correctly generated."""
        url = self.ws.get_authors_page('Jon Snow')
        self.assertEqual('http://techcrunch.com/author/jon-snow', url)

    def test_techcrunch_get_existing_author(self):
        """Tests if an author's information can be found by his/her name."""

        # If an author is already stored, the function doesn't need to find 
        # more informations about him/her.
        name = 'Jon Snow'
        Author.objects.create(name = name, outlet_id = self.ws.outlet.id)
        result = self.ws.get_author(name, '')

        self.assertEqual(result, {'name': 'Jon Snow'})

    def test_techcrunch_extract_author(self):
        """Tests if an author's information can be extracted from his page."""
        parsed = parse_html('author.html')
        result = self.ws.extract_author(parsed)
        result = list(result.keys())
        expected = ['twitter', 'linkedin', 'about', 'profile', 'avatar']

        self.assertEqual(result, expected)

    def test_techcrunch_extract_articles(self):
        """Tests if an article list can be extracted from xml feed."""

        # Add these author just to prevent `get_author` method from fetching
        # their info on the internet.
        authors = ['Ron Miller', 'Jonathan Shieber', 'Josh Constine',
                   'Anthony Ha', 'Sarah Perez', 'Connie Loizos',
                   'Darrell Etherington', 'Alex Wilhelm', 'Jon Russell',
                   'Khaled Hamze', 'Katie Roof', 'Brian Heater',
                   'Danny Crichton', 'Taylor Hatmaker', 'Devin Coldewey']

        for name in authors:
            Author.objects.create(name = name, outlet_id = self.ws.outlet.id)

        results = self.ws.extract_articles(self.articles_tree)

        self.assertEqual(len(results), 20)