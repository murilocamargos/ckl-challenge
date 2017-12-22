from django.test import TestCase
from articles import utils
from lxml import etree
import os

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