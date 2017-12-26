from articles.utils import create_article
from articles.models import Outlet, Author

from lxml import etree, html
import requests

class WebScraper(object):
    """This class provides some helpful method to scraping web content."""

    def __init__(self, slug = None):
        # Find current outlet by given slug
        if slug:
            self.outlet = Outlet.objects.filter(slug = slug).first()

    def download(self, url, content_type = 'xml'):
        """This method downloads and parses a url with a given type."""
        tree = None

        if content_type == 'xml':
            tree = etree.parse(url)

        elif content_type == 'html':
            response = requests.get(url)
            tree = html.fromstring(response.content)

        return tree

    def classify_links(self, links):
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

    def html_to_string(self, item):
        """This method return the html representation of a lxml item."""
        return html.tostring(item).decode('utf8')

    def get_articles(self):
        """
        This function downloads a given outlet's articles and call its
        extraction method.
        """
        parsed = self.download(self.feed_url, self.feed_type)
        if not parsed:
            return []

        articles = self.extract_articles(parsed)
        
        return [create_article(self.outlet, art) for art in articles]

    def get_author(self, author_name, article_url):
        """
        This method fetches an author's information by his/her name. If this
        author is already stored, there is no necessity of looking its profile
        page.

        If his twitter handle is not found, we can check the possibility of
        finding it in the article's page.
        """
        search = Author.objects.filter(
            name = author_name,
            outlet_id = self.outlet.id
        ).count()

        author = {}
        
        if search == 0:
            # Download and parse html author's page
            author_url = self.get_authors_page(author_name)
            parsed = self.download(author_url, self.author_page_type)

            # Extract wanted information from his/her page
            author = self.extract_author(parsed)

            # Check the article's page for his/her twitter if needed
            if not 'twitter' in author:
                parsed = self.download(article_url, self.article_page_type)
                author['twitter'] = self.extract_twitter(parsed, author_name)

        author['name'] = author_name

        return author