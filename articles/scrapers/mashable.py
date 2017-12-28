import django.template.defaultfilters as filters

from articles.scrapers.scraper import WebScraper
from articles.models import Article

import re, dateutil.parser

class Mashable(WebScraper):
    """
    This class provides the required methods to scrape an article from
    Mashable outlet.
    """
    
    def __init__(self):
        # Some initial parameters for scraping articles and authors
        self.outlet_slug = 'mashable'
        self.feed_url = 'mashabletech'
        self.feed_type = 'twitter'
        self.author_page_type = 'html'
        self.article_page_type = 'html'

        super(Mashable, self).__init__(self.outlet_slug)


    def get_authors_page(self, author_name):
        """
        This method provides the author's profile url, the url can be set
        previously at the `author_url` attribute; but it can only be used once.
        """

        if hasattr(self, 'author_url') and self.author_url != '':
            # Use and remove `author_url`
            url, self.author_url = self.author_url, ''

            return url

        return 'http://mashable.com/author/' + filters.slugify(author_name)


    def article_info(self, parsed):
        """
        All the information needed do add an article can be found in the
        article's page except the author's which will be fetched at another
        page.
        """

        data = {}


        # Gets the title, url, pub_date and author's name in the metatags
        title_xpath = 'meta[@property="og:title"]'
        title = self.get_text_or_attr(parsed, title_xpath, 'content')


        url_xpath = 'meta[@property="og:url"]'
        url = self.get_text_or_attr(parsed, url_xpath, 'content')


        date_xpath = 'meta[@property="og:article:published_time"]'
        date = self.get_text_or_attr(parsed, date_xpath, 'content')


        author_xpath = 'meta[@name="author"]'
        author = self.get_text_or_attr(parsed, author_xpath, 'content')


        if not title or not url or not date or not author:
            return {}


        data['title'] = title
        data['url'] = self.remove_query(url)


        # Check if article already exists
        if Article.objects.filter(url = data['url']).count() > 0:
            return {}
        

        # Tries to parse date element
        try:
            data['date'] = dateutil.parser.parse(date)
        except:
            pass


        thumb_xpath = 'meta[@property="og:image"]'
        thumb = self.get_text_or_attr(parsed, thumb_xpath, 'content')
        if thumb:
            data['thumb'] = thumb
        

        categories_xpath = 'meta[@name="keywords"]'
        categories = self.get_text_or_attr(parsed, categories_xpath, 'content')
        if categories:
            data['categories'] = [filters.title(c) for c in categories.split(', ')]


        # Add an author name to the list of authors
        data['authors'] = [{
            'name': author
        }]


        # Tries to find his profile page
        page_xpath = 'span[@class="author_name"]/a'
        page = self.get_text_or_attr(parsed, page_xpath, 'href')

        if page:
            page = 'http://mashable.com/' + page
        else:
            page = 'http://mashable.com/author/' + filters.slugify(author)

        # Set his profile page as the url to be fetched by `get_author`
        self.author_url = page
        author = self.get_author(author)

        data['authors'][0].update(author)


        # Get article's content
        xpath = './/section[@class="article-content blueprint"]/p'
        items = parsed.xpath(xpath)
        data['content'] = self.clear_text(items)


        return data


    def extract_articles(self, statuses):
        """
        This method formats Mashable's articles, categories and authors to
        store them in DB; its return should be a list of dictionaries in the
        form given in utils' function `create_article`.
        """

        for status in statuses:
            link = None

            # Tries to find the word `mash` on status url. If the url doesn't
            # have it, it could lead to a twitter status over the article's page
            for url in status.urls:
                if 'mash' in url.expanded_url:
                    link = url.expanded_url

            if not link:
                continue


            # Downloads and parses the article's page
            parsed = self.parse(link, self.article_page_type)
            article = self.article_info(parsed)


            if article == {}:
                continue


            # In case there is no pub_date in the article's page, use the pub
            # date of the twitter status itself.
            if 'date' not in article:
                try:
                    article['date'] = dateutil.parser.parse(status.created_at)
                except:
                    continue


            yield article


    def extract_author(self, parsed, author_name = ''):
        """
        This method extract all important informations about an author. These
        informations can be found by its xpath.
        
        A simple way to find the xpath of a given element is using the browser's
        inspection mode. Chrome has a feature of copying the inspected element's
        xpath.
        """

        author = {}

        # Find all links with this xpath and tries to classify them
        links_xpath = 'div[@class="profile-networks"]/a'
        links = self.get_text_or_attr(parsed, links_xpath, 'href')
        
        for social in self.classify_links(links):
            author[social[0]] = social[1]


        # Get description text provided by the author
        xpath = './/div[@class="profile-about"]'
        items = parsed.xpath(xpath)
        author['about'] = self.clear_text(items)


        # Get Mashable url profile
        profile = self.get_text_or_attr(parsed, 'figure/a', 'href')
        if profile:
            author['profile'] = profile


        # Get his/her avatar url
        avatar = self.get_text_or_attr(parsed, 'figure/a/img', 'src')
        if avatar:
            author['avatar'] = avatar


        return author