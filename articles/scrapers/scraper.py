import json
import os
import re
import twitter
import dateutil.parser
import requests

from lxml import etree, html

from django.template.defaultfilters import slugify, title
from django.utils.html import strip_tags

from articles.models import Author, Category, Outlet, Article

EXCEPTIONS = {
    'feed': 'You must set the articles\' feed configs (i.e. url and type).',
    'extract_method': 'Scraper must provide an `extract_articles` method.',
    'download': 'A parsing method was not implemented for this data type.',
    'not_parsed': 'The available method couldn\'t parse your url.',
    'unacceptable': 'There are unacceptable attributes on your request.',
    'required': 'You must provide all required parameters to add an article.',
    'outlet': 'You must provide an outlet to create articles.',
    'nsmap': 'The namespace must be a dictionary.',
    'author': 'You must set the authors\' page configs (i.e. url and type).',
    'extract_author': 'Scraper must provide an `extract_author` method.',
    'get_authors_page': 'Scraper must provide an `get_authors_page` method.',
}

class WebScraper(object):
    """This class provides some helpful method to scraping web content."""

    def __init__(self, name=None):
        # Find current outlet by given name

        self.feed_url = None
        self.feed_type = None
        self.author_page_type = None
        self.outlet = None
        self.nsmap = None

        if name:
            self.outlet = Outlet.objects.filter(name=name).first()


    def extract_articles(self, data):
        """
        Any scraper derived from this class should implement a method called
        extract_articles in order to parse the feed_url.
        """
        raise NotImplementedError(EXCEPTIONS['extract_method'])


    def get_authors_page(self, author_name):
        """
        Any scraper derived from this class should implement a method called
        get_authors_page to provide the author's page URL.
        """
        raise NotImplementedError(EXCEPTIONS['get_authors_page'])


    def extract_author(self, data, author_idx=0):
        """
        Any scraper derived from this class should implement a method called
        extract_author to provide the author's page URL.
        """
        raise NotImplementedError(EXCEPTIONS['get_authors_page'])


    def create_article(self, data):
        """
        This function creates an article with all its attributes such as its
        author and categories. The data will be checked to make sure no
        unacceptable input comes in and every required attribute is met.
        """

        if not hasattr(self, 'outlet'):
            raise ValueError(EXCEPTIONS['outlet'])

        if not isinstance(self.outlet, Outlet):
            raise ValueError(EXCEPTIONS['outlet'])

        self.check_data(data)

        # Form a dictionary with all article's information but its `url`, the
        # article's information can be seen as anything whose type is str
        # inside `data`. However, `date` does not live up by this rule, so we
        # add it manually to article_def.
        url = data.pop('url')

        # Get exiting categories from data, if the article has just one, it
        # will come as str; in that case, convert it to a unitary list.
        categories = []

        if 'categories' in data:
            categories = data.pop('categories')

            if isinstance(categories, str):
                categories = [categories]


        # After removing the url and categories from data, we can parse the
        # dictionary for string values. Every string value should be an article
        # property.
        article = {key: data[key] for key in data if isinstance(data[key], str)}
        article['date'] = data.pop('date')
        article['outlet_id'] = self.outlet.id

        article, _ = Article.objects.get_or_create(
            url=url,
            defaults=article
        )


        # Store non existing authors and assign them to the article
        for author_info in data['authors']:

            # Form a dictionary with all author's information but his/her name
            author = {k: author_info[k] for k in author_info if k != 'name'}

            author, _ = Author.objects.get_or_create(
                name=author_info['name'],
                outlet_id=self.outlet.id,
                defaults=author
            )

            article.authors.add(author)


        # Store non existing categories and assign them to the article
        for cat_name in categories:
            category, _ = Category.objects.get_or_create(
                slug=slugify(cat_name),
                defaults={
                    'name': title(cat_name)
                }
            )

            article.categories.add(category)


        return article


    def get_articles(self):
        """
        This function downloads a given outlet's articles and call its
        extraction method.
        """

        # Verify if the class calling this method provides an articles' feed
        # for fetching articles.
        if not self.feed_url or not self.feed_type:
            raise TypeError(EXCEPTIONS['feed'])


        # Download and parse the articles' feed
        parsed = self.parse(self.feed_url, self.feed_type)
        if parsed is None:
            raise TypeError(EXCEPTIONS['not_parsed'])


        # The parsed feed will be inputed to the article extractor who will
        # yield every article it can find and process.
        results = []

        for article_info in self.extract_articles(parsed):
            article = self.create_article(article_info)
            results += [article]
            print(article)

        return results


    def get_author(self, author_name, author_idx=0):
        """
        This method fetches an author's information by his/her name. If this
        author is already stored, there is no necessity of looking its profile
        page.
        """

        # Verify if the class calling this method provides the methods for
        # downloading, parsing and filtering the author's information.
        if not self.outlet:
            raise TypeError(EXCEPTIONS['outlet'])

        if not self.author_page_type:
            raise TypeError(EXCEPTIONS['author'])


        search = Author.objects.filter(
            name=author_name,
            outlet_id=self.outlet.id
        ).count()


        author = {
            'name': author_name,
        }


        if search == 0:
            # Download and parse html author's page
            author_url = self.get_authors_page(author_name)
            parsed = self.parse(author_url, self.author_page_type)

            # Extract wanted information from his/her page
            author.update(self.extract_author(parsed, author_idx))


        return author


    def get_text_or_attr(self, item, key, attr=None):
        """
        This function returns a string or a list of strings containing
        the text inside or an attribute value of lxml Elements.

        Args:
            item: must be an Element from a lxml parsing.
            key:  it's the name of children tags to find.
            attr: if this is provided, the attribute `attr` will be fetched
                  instead of the text.
        """

        # This namespace mapping may change with different outlets, that why
        # this method cannot be static.
        nsmap = {
            'dc': 'http://purl.org/dc/elements/1.1/',
            'media': 'http://search.yahoo.com/mrss/',
            'feedburner': 'http://rssnamespace.org/feedburner/ext/1.0',
        }

        if hasattr(self, 'nsmap'):
            if self.nsmap and not isinstance(self.nsmap, dict):
                raise ValueError(EXCEPTIONS['nsmap'])

            if self.nsmap:
                nsmap.update(self.nsmap)


        # Searches for a given key on parsed document's root
        search = item.xpath('.//' + key, namespaces=nsmap)


        found = len(search)
        items = []
        if found > 0:
            if attr:
                items = [item.get(attr) for item in search]
            else:
                items = [item.text for item in search]


        # Retrieve item itself if there's only one in the list
        if len(items) == 1:
            return items[0]


        return items


    @staticmethod
    def html_to_string(item):
        """This method return the html representation of a lxml item."""
        return html.tostring(item).decode('utf8')


    @staticmethod
    def remove_query(url):
        """This function removes anything after `?` from a string."""
        if isinstance(url, str):
            return url.split('?')[0]


    @staticmethod
    def parse(url, content_type='xml'):
        """This method downloads and parses a url with a given type."""

        if content_type == 'xml':
            response = requests.get(url)
            return etree.fromstring(response.content)


        elif content_type == 'html':
            response = requests.get(url)
            return html.fromstring(response.content)


        elif content_type == 'json':
            response = requests.get(url)
            return json.loads(response.text)


        elif content_type == 'twitter':
            api = twitter.Api(
                consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
                consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
                access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
            )

            return api.GetUserTimeline(screen_name=url)

        raise NotImplementedError(EXCEPTIONS['parse'])


    @staticmethod
    def classify_links(links):
        """This method tries to classify some known social network urls."""

        results = []

        for link in links:
            if 'http' not in link:
                # We don't want relative urls
                continue

            elif 'twitter.com' in link:
                results += [('twitter', link)]

            elif 'linkedin.com' in link:
                results += [('linkedin', link)]

            elif 'facebook.com' in link:
                results += [('facebook', link)]

            else:
                results += [('website', link)]

        return results


    @staticmethod
    def check_data(data):
        """
        This function checks the data integrity of `create_article` function's
        input. We check for required and accepted parameters.
        """
        required = {
            'article': ['title', 'url', 'date', 'content', 'authors'],
            'authors': ['name']
        }

        accepted = {
            'article': required['article'] + ['categories', 'thumb'],
            'authors': required['authors'] + ['twitter', 'avatar', 'facebook',\
                'linkedin', 'about', 'profile', 'website']
        }


        # Check first level dictionary keys
        req = required['article'][::]

        for key in data:
            if key not in accepted['article']:
                raise ValueError(EXCEPTIONS['unacceptable'])

            if key in required['article']:
                req.remove(key)

        count_req = len(req)
        if count_req > 0:
            raise ValueError(EXCEPTIONS['required'])


        # Check second level dictionary keys (authors)
        for author in data['authors']:

            req = required['authors'][::]

            for key in author:
                if key not in accepted['authors']:
                    raise ValueError(EXCEPTIONS['unacceptable'])

                if key in required['authors']:
                    req.remove(key)

            count_req = len(req)
            if count_req > 0:
                raise ValueError(EXCEPTIONS['required'])


        # Check if there are any authors on data
        count_authors = len(data['authors'])
        if not 'authors' in data or count_authors == 0:
            raise ValueError(EXCEPTIONS['required'])


    @staticmethod
    def clear_text(items):
        """
        Tries to get a clean text (i.e. without html tags and double spaces)
        from a given xpath items.
        """

        if not isinstance(items, list):
            items = [items]

        content = ''

        for item in items:

            # Convert lxml item in string with html tags
            if isinstance(item, html.HtmlElement):
                item = WebScraper.html_to_string(item)

            if isinstance(item, etree._Element):
                item = item.text

            if item is not None:
                # Remove html tags
                content += strip_tags(item) + ' '

        # Remove break lines
        content = re.sub('[\n\t]', '', content)

        # Remove double spaces
        content = re.sub('[ ]{2,}', ' ', content).strip()

        return content


    @staticmethod
    def parse_datetime_passing_errors(date):
        """Tries to parse a datetime without raising any error."""
        try:
            return dateutil.parser.parse(date)
        except ValueError:
            return None
        except TypeError:
            return None

        return None
