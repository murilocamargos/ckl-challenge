from django.test import TestCase
from articles import utils
from lxml import etree
from articles.models import Outlet, Author, Category, Article
import os, dateutil.parser

current_path = os.path.dirname(__file__)

class UtilsTestCase(TestCase):
    """This class defines the test suite for the utility functions."""

    def setUp(self):
        """Defines the test client and other test variables."""
        # Load and parse an existing xml example file
        file = os.path.join(current_path, 'files/techcrunch_articles.xml')
        self.tree = etree.parse(file)

        self.article_data = {
            'title': 'My article',
            'url': 'http://www.myarticle.com.br',
            'date': dateutil.parser.parse('Fri, 22 Dec 2017 17:21:29 +0000'),
            'content': 'The article\'s content.',
            'authors': [
                {'name': 'Murilo Camargos'},
            ],
        }

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

    def test_utils_check_data_correct(self):
        """Tests if data is correctly checked for article creation."""
        self.assertEqual(utils.check_data(self.article_data), True)

    def test_utils_check_data_remove_required(self):
        """Tests if data check raises exception after removing required."""
        msg = 'You must provide all required parameters to add an article.'

        # Remove title (required)
        del self.article_data['title']
        with self.assertRaisesMessage(ValueError, msg):
            utils.check_data(self.article_data)

        # Put title back in and add an author without name
        self.article_data['title'] = 'Title returns'
        self.article_data['authors'] += [{'linkedin': 'johndoe'}]
        with self.assertRaisesMessage(ValueError, msg):
            utils.check_data(self.article_data)

    def test_utils_check_data_add_unaccepted(self):
        """Tests if data check raises exception after adding unaccepted."""
        msg = 'There are unacceptable attributes on your request.'

        self.article_data['stranger'] = 'things'
        with self.assertRaisesMessage(ValueError, msg):
            utils.check_data(self.article_data)

        # Remove `stranger` from `data` and use `John` attribute in author
        del self.article_data['stranger']
        self.article_data['authors'][0]['John'] = 'Doe'
        with self.assertRaisesMessage(ValueError, msg):
            utils.check_data(self.article_data)

    def test_utils_create_article(self):
        """
        Tests if article creator helper is adding an article and its properties
        such as categories and author.
        """

        outlet = Outlet.objects.create(name = 'TechCrunch')

        # This is all the necessary information to create an article
        article = {
            'title': 'My article',
            'url': 'http://www.myarticle.com.br',
            'date': dateutil.parser.parse('Fri, 22 Dec 2017 17:21:29 +0000'),
            'content': 'The article\'s content.',
            'authors': [
                {'name': 'Murilo Camargos'},
                {'name': 'John Kennedy'}
            ],
            'categories': ['IT', 'Django', 'it']
        }

        article = utils.create_article(outlet, article)

        # Check if article is an Article object
        self.assertEqual(isinstance(article, Article), True)
        self.assertEqual(Article.objects.count(), 1)

        # Check if categories were created. It is only two because two
        # categories on the list has the same slug, so the relationship
        # won't be added twice.
        self.assertEqual(Category.objects.count(), 2)

        # Check if author was created
        self.assertEqual(Author.objects.count(), 2)

    def test_utils_create_article_author(self):
        """
        Tests if article creator helper is adding all the attributes of its
        author.
        """

        outlet = Outlet.objects.create(name = 'TechCrunch')

        # This is all the necessary information to create an article
        article = {
            'title': 'My article',
            'url': 'http://www.myarticle.com.br',
            'date': dateutil.parser.parse('Fri, 22 Dec 2017 17:21:29 +0000'),
            'content': 'The article\'s content.',
            'authors': [
                {
                    'name': 'Murilo Camargos',
                    'profile': 'mcam',
                    'twitter': 'mcam',
                    'linkedin': 'mcam',
                    'facebook': 'mcam',
                    'website': 'mcam',
                    'avatar': 'mcam',
                    'about': 'Bla Bla Bla',
                },
            ],
            'categories': ['IT', 'Django'],
        }

        article = utils.create_article(outlet, article)

        # Check if the author was created with all properties defined
        self.assertEqual(Author.objects.filter(profile = 'mcam').count(), 1)
        self.assertEqual(Author.objects.filter(twitter = 'mcam').count(), 1)
        self.assertEqual(Author.objects.filter(linkedin = 'mcam').count(), 1)
        self.assertEqual(Author.objects.filter(facebook = 'mcam').count(), 1)
        self.assertEqual(Author.objects.filter(website = 'mcam').count(), 1)
        self.assertEqual(Author.objects.filter(avatar = 'mcam').count(), 1)
        self.assertEqual(Author.objects.filter(about__contains = 'Bla').count(), 1)