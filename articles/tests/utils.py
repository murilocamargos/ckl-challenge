from django.test import TestCase
from articles import utils
from lxml import etree
from articles.models import Outlet, Author, Category, Article
import os, dateutil.parser

class UtilsTestCase(TestCase):
    """This class defines the test suite for the utility functions."""

    def setUp(self):
        """Defines the test client and other test variables."""
        # Load and parse an existing xml example file
        file = os.path.join(os.path.dirname(__file__), 'files/example.xml')
        self.tree = etree.parse(file)

    def test_utils_remove_query(self):
        """Tests if query is removed from a given url."""
        url = 'https://www.google.com.br/?gws_rd=cr&dcr=0&ei=OEI9Wpr0HMeNwwSF6IGAAQ'
        self.assertEqual(utils.remove_query(url), 'https://www.google.com.br/')

    def test_utils_get_text_or_attr(self):
        """Tests if function is getting text or attribute from, given an lxml
           Item's key"""

        # Find the first element tagged `item` from the xml file
        item = self.tree.xpath("//item")[0]

        # Get text from the item's child named `title`
        title = utils.get_text_or_attr(item, 'title')
        self.assertEqual(title, 'That time I got locked out of my Google account for a month')

        # Get list of texts from the item's children named `category`
        categories = utils.get_text_or_attr(item, 'category')
        self.assertEqual(categories, ['Cloud', 'Drama', 'Security', 'TC', 'Google', 'gmail'])

        # Get attribute named `url` from the item's children named `media:thumbnail`
        thumbs = utils.get_text_or_attr(item, 'media:thumbnail', 'url')
        self.assertEqual(thumbs, ['https://tctechcrunch2011.files.wordpress.com/2017/12/gettyimages-170409877.jpg?w=210&h=158&crop=1', 'https://tctechcrunch2011.files.wordpress.com/2017/12/gettyimages-170409877.jpg'])

    def test_utils_create_article(self):
        """Tests if article creator helper is adding an article and its
           properties such as categories and author."""
        outlet = Outlet.objects.create(name = 'TechCrunch')
        article = {
            'title': 'My article',
            'url': 'http://www.myarticle.com.br',
            'date': dateutil.parser.parse('Fri, 22 Dec 2017 17:21:29 +0000'),
            'thumb': 'thumbnail.jpg',
            'content': 'Article\'s content',
            'author': {
                'name': 'Murilo Camargos',
                'avatar': ''
            },
            'categories': ['IT', 'Django']
        }

        article = utils.create_article(outlet, article)

        # Check if article if an Article object
        self.assertEqual(isinstance(article, Article), True)
        self.assertEqual(Article.objects.count(), 1)

        # Check if categories were created
        self.assertEqual(Category.objects.count(), 2)

        # Check if author was created
        self.assertEqual(Author.objects.count(), 1)