from django.template.defaultfilters import slugify

from articles.scrapers.scraper import WebScraper
from articles.utils import get_text_or_attr, remove_query
from articles.models import Article

import re, dateutil.parser

class CheesecakeLabs(WebScraper):
    """
    This class provides the required methods to scrape an article from
    CheesecakeLabs outlet. The articles are fetched from their Google+ account.
    """
    def __init__(self):
        # Some initial parameters for scraping articles and authors
        self.outlet_slug = 'cheesecake-labs'
        self.feed_url = 'https://www.googleapis.com/plus/v1/people/117441029475835978521/activities/public/?key=AIzaSyDlMlRdHLNCDQESKRt6o67jyCmRA1HlGmQ'
        self.feed_type = 'json'
        self.article_page_type = 'html'

        super(CheesecakeLabs, self).__init__(self.outlet_slug)

    def get_from_url(self, url):
        """Downloads and parses article's page."""
        parsed = self.download(url, self.article_page_type)
        return self.article_info(parsed)

    def article_info(self, parsed):
        """
        All the information needed do add an article can be found in the
        article's page itself. This method extracts these information using the 
        xpath.
        """
        data = {}

        # If there is no title, it is possible that we're parsing the wrong
        # page (e.g. Youtube's)
        data['title'] = get_text_or_attr(parsed, 'h1[@class="entry__title"]')
        if data['title'] == []:
            return {}

        xpath = 'div[@class="post-categories"]/a'
        data['categories'] = get_text_or_attr(parsed, xpath)
        
        xpath = 'img[@class="cover-media"]'
        data['thumb'] = get_text_or_attr(parsed, xpath, 'src')

        # Tries to parse date element
        pub_date = get_text_or_attr(parsed, 'time', 'datetime')
        try:
            data['date'] = dateutil.parser.parse(pub_date)
        except:
            pass

        # Get article's contents
        content = parsed.xpath('.//div[@class="entry__content "]')
        if content:
            data['content'] = self.html_to_string(content[0]).strip()

        # Find authors
        data['authors'] = []
        authors = parsed.xpath('.//span[@class="author vcard"]')
        about_xpath = './/div[@class="author-description"]/p[2]'
        for author in authors:
            data['authors'].append({
                'profile': get_text_or_attr(author, 'a', 'href'),
                'avatar': get_text_or_attr(author, 'img', 'src'),
                'name': get_text_or_attr(author, 'img', 'alt'),
                'about': get_text_or_attr(parsed, about_xpath)
            })

        return data

    def extract_articles(self, data):
        """
        This method formats CheesecakeLabs's articles, categories and authors to
        store them in DB; its return should be a list of dictionaries in the
        form given in utils' function `create_article`.

        Google's API result is a JSON.
        """
        for item in data['items']:
            url = None

            # We need these attributes on Google's JSON
            if 'published' not in item or 'object' not in item:
                continue

            # If there is no attachments in item, it could be just a note
            if 'attachments' not in item['object']:
                # If it is a note, tries to find a cheesecakelabs url in it
                if item['object']['objectType'] == 'note':
                    pattern = 'cheesecakelabs\.com[^"]{1,}'
                    urls = re.findall(pattern, item['object']['content'])
                    if urls:
                        url = 'http://' + urls[0]
                else:
                    continue

            else:
                # We just need a url
                for attach in item['object']['attachments']:
                    if attach['objectType'] == 'article':
                        break

                if 'url' not in attach:
                    continue

                url = remove_query(attach['url'])

            # We don't want to add again an article, so we search for it
            if Article.objects.filter(url = url).count() > 0:
                continue

            # Fetch article's information directly from CheesecakeLabs blog
            article = self.get_from_url(url)

            if article == {}:
                continue

            article['url'] = url

            # If there's no pub_date on cheesecake post, try to use `published`
            # from Google
            if 'date' not in article:
                try:
                    article['date'] = dateutil.parser.parse(item['published'])
                except:
                    article = {}

            yield article