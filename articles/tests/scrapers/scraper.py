from mock import patch
import dateutil.parser

from django.test import TestCase

from articles.models import Outlet, Author, Category, Article
from articles.tests.utils import get_file, parse_mocked
from articles.scrapers.scraper import WebScraper

class WebScraperTestCase(TestCase):
    """This class defines the test suite for the web scrapers."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.scraper = WebScraper()

        self.article_data = {
            'title': 'Atomic Design with React',

            'url': 'https://cheesecakelabs.com/blog/atomic-design-react/',

            'date': dateutil.parser.parse('Fri, 8 Dec 2017 16:11:37 +0000'),

            'content': 'How one methodology allowed me to create a great \
                design system from scratch and made me a better developer, \
                with principles of componentization, hierarchies and reuses \
                of code.',

            'authors': [
                {'name': 'Danilo Woznica'},
                {'name': 'Francieli Lima'}
            ],

            'categories': [
                {'name': 'Front-end'},
                {'name': 'Design'}
            ]
        }


    @patch('requests.get')
    def test_ws_parse_xml(self, mock_get):
        """Tests if parsing method can parse xml with mocked data."""
        mock_get.return_value.content = get_file('example.xml')

        parsed = self.scraper.parse('url:example.xml', 'xml')

        self.assertNotEqual(parsed, None)
        self.assertEqual(len(parsed.getchildren()), 21)


    @patch('requests.get')
    def test_ws_parse_html(self, mock_get):
        """Tests if parsing method can parse html with mocked data."""
        mock_get.return_value.content = get_file('example.html')

        parsed = self.scraper.parse('url:example.html', 'html')

        self.assertNotEqual(parsed, None)
        self.assertEqual(len(parsed.getchildren()), 2)


    @patch('requests.get')
    def test_ws_parse_json(self, mock_get):
        """Tests if parsing method can parse json with mocked data."""
        mock_get.return_value.text = get_file('example.json')

        parsed = self.scraper.parse('url:example.json', 'json')

        self.assertNotEqual(parsed, None)
        self.assertEqual(len(parsed), 6)


    def test_ws_classify_links(self):
        """Tests link cleaning."""
        links = [
            'http://www.facebook.com/matthew.panzarino',
            'http://twitter.com/Panzer',
            'https://www.linkedin.com/in/matthewpanzarino',
            '/author/matthew-panzarino/feed/',
            'http://th.linkedin.com/in/jmarussell'
        ]

        results = self.scraper.classify_links(links)

        self.assertEqual(results, [
            ('facebook', 'http://www.facebook.com/matthew.panzarino'),
            ('twitter', 'http://twitter.com/Panzer'),
            ('linkedin', 'https://www.linkedin.com/in/matthewpanzarino'),
            ('linkedin', 'http://th.linkedin.com/in/jmarussell')
        ])


    @patch('requests.get')
    def test_ws_html_to_string(self, mock_get):
        """Test if html conversion of a lxml item is working correctly."""
        mock_get.return_value.content = get_file('example.html')

        parsed = self.scraper.parse('url:example.html', 'html')

        # Search for h2 tags inside anything with id equals to `latest`
        find_item = parsed.xpath('//h2[@class="section__title"]')
        result = ''
        if find_item:
            result = self.scraper.html_to_string(find_item[0]).strip()

        expected = '<h2 class="section__title">Social Networks</h2>'

        self.assertEqual(result, expected)


    def test_ws_remove_query(self):
        """Tests if query is removed from a given url."""
        url = 'https://www.google.com.br/?gws_rd=cr&dcr=0&ei=OEI9Wpr0HMeNwwSF6'

        result = self.scraper.remove_query(url)

        expected = 'https://www.google.com.br/'

        self.assertEqual(result, expected)


    def test_ws_check_data_correct(self):
        """Tests if data is correctly checked for article creation."""
        self.assertEqual(self.scraper.check_data(self.article_data), None)


    def test_ws_check_data_rm_required(self):
        """Tests if data check raises exception after removing required."""
        msg = 'You must provide all required parameters to add an article.'

        # Remove title (required)
        del self.article_data['title']

        with self.assertRaisesMessage(ValueError, msg):
            self.scraper.check_data(self.article_data)

        # Put title back in and add an author without name
        self.article_data['title'] = 'Title returns'
        self.article_data['authors'] += [{'linkedin': 'johndoe'}]

        with self.assertRaisesMessage(ValueError, msg):
            self.scraper.check_data(self.article_data)


    def test_ws_check_data_rm_author(self):
        """Tests if data check raises exception after removing required."""
        msg = 'You must provide all required parameters to add an article.'

        # Empty author list
        self.article_data['authors'] = []

        with self.assertRaisesMessage(ValueError, msg):
            self.scraper.check_data(self.article_data)

        # Remove author list from dictionary
        del self.article_data['authors']

        with self.assertRaisesMessage(ValueError, msg):
            self.scraper.check_data(self.article_data)


    def test_ws_check_data_unaccepted(self):
        """Tests if data check raises exception after adding unaccepted."""
        msg = 'There are unacceptable attributes on your request.'

        self.article_data['stranger'] = 'things'

        with self.assertRaisesMessage(ValueError, msg):
            self.scraper.check_data(self.article_data)

        # Remove `stranger` from `data` and use `John` attribute in author
        del self.article_data['stranger']
        self.article_data['authors'][0]['John'] = 'Doe'

        with self.assertRaisesMessage(ValueError, msg):
            self.scraper.check_data(self.article_data)


    @patch('requests.get')
    def test_ws_get_text_or_attr(self, mock_get):
        """Tests if function is getting text or attribute from, given an lxml
           Item's key"""

        mock_get.return_value.content = get_file('feed.xml')

        parsed = self.scraper.parse('url:feed.xml', 'xml')

        # Find the first element tagged `item` from the xml file
        item = parsed.xpath("//item")[0]

        # Get text from the item's child named `title`
        title = self.scraper.get_text_or_attr(item, 'title')
        self.assertEqual(title, 'That time I got locked out of my Google account for a month')

        # Get list of texts from the item's children named `category`
        categories = self.scraper.get_text_or_attr(item, 'category')
        self.assertEqual(categories, ['Cloud', 'Drama', 'Security', 'TC', 'Google', 'gmail'])

        # Get attribute named `url` from the item's children named `media:thumbnail`
        thumbs = self.scraper.get_text_or_attr(item, 'media:thumbnail', 'url')
        self.assertEqual(thumbs, ['https://tctechcrunch2011.files.wordpress.com/2017/12/gettyimages-170409877.jpg?w=210&h=158&crop=1', 'https://tctechcrunch2011.files.wordpress.com/2017/12/gettyimages-170409877.jpg'])


    def test_ws_create_article(self):
        """
        Tests if article creator helper is adding an article and its properties
        such as categories and author.
        """
        self.scraper.outlet = Outlet.objects.create(name='Fictional Outlet')

        article = self.scraper.create_article(self.article_data)

        # Check if article is an Article object
        self.assertEqual(isinstance(article, Article), True)
        self.assertEqual(Article.objects.count(), 1)

        # Check if categories were created. It is only two because two
        # categories on the list has the same slug, so the relationship
        # won't be added twice.
        self.assertEqual(Category.objects.count(), 2)

        # Check if author was created
        self.assertEqual(Author.objects.count(), 2)


    def test_ws_create_article_author(self):
        """
        Tests if article creator helper is adding all the attributes of its
        author.
        """
        self.scraper.outlet = Outlet.objects.create(name='Fictional Outlet')

        author_data = {
            'profile': 'https://cheesecakelabs.com/br/blog/author/danilo',
            'linkedin': 'https://br.linkedin.com/in/danilowoz',
            'facebook': 'https://www.facebook.com/danilowoz',
            'website': 'https://www.behance.net/danilowoz',
            'avatar': 'https://s3.amazonaws.com/ckl-website-static/wp-content/uploads/2017/12/IMG_8639-300x300.jpg',
            'about': 'Likes to convert coffee and music into great interfaces \
                and many lines of code to solve bigs problems or open source \
                projects.',
        }

        # Add article with updated author data
        self.article_data['authors'][0].update(author_data)
        self.scraper.create_article(self.article_data)

        # Get all fields from the first author with name containing Danilo
        author = Author.objects.filter(name__contains='Danilo').first()
        fields = author._meta.get_fields()
        result = {f.name: getattr(author, f.name, None) for f in fields}

        # Verify if everything in author_data was added to author Danilo
        for key in author_data:
            self.assertEqual(author_data[key], result[key])


    def test_ws_clear_text(self):
        """Tests if lxml items are begin correctly cleaned and merged."""
        parsed = parse_mocked('cheesecakelabs_article.html', 'html')


        # Xpath for paragraph tags on content div
        xpath = './/div[@class="entry__content "]/p'

        # Gets just the third and fourth p tags to test
        third_fourth = parsed.xpath(xpath)[2:4]

        # Clear text from them
        cleared = self.scraper.clear_text(third_fourth)

        content = 'This is all reflected in our great ratings and reviews featured on Cheesecake Labs profile on Clutch with client reviews. The B2B research platform&#8217;s ratings and reviews include a combination of metrics, ranging from experience in the sector and market presence to types of clients and ability to deliver awesome results delivered to clients. Furthermore, Clutch&#8217;s dedicated analysts interviewed our current and past clients to accurately portray our strengths on our profile. We are excited to celebrate these accomplishments and our great clients who showed their appreciation for our work. These honors would not have been possible without the time they took to provide their detailed client reviews.'

        self.assertEqual(cleared, content)
