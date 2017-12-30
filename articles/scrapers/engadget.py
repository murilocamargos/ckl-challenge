from django.template.defaultfilters import slugify

from articles.scrapers.scraper import WebScraper
from articles.models import Article

import re, dateutil.parser, urllib.parse

class Engadget(WebScraper):
    """
    This class provides the required methods to scrape an article from Engadget
    outlet. Fetching an article from Engadget follows the above steps:

    1) Download the Engadget XML feed at `feed_url`

    2) Go through every item on this feed and for each one extract informations
       such as title, url, pub_date, categories, content, thumb and authors.

    3) Luckily, all the article's information can be fetched from this source;
       but not the author's. Step 3 is called inside step's 2 method to get
       information about the author(s).

    4) If the author's twitter handle can't be found at hist page, we go back
       to the article's page and try to find it there.

    """
    
    def __init__(self):
        # Some initial parameters for scraping articles and authors
        self.outlet_name = 'Engadget'
        self.feed_url = 'http://www.engadget.com/rss.xml'
        self.feed_type = 'xml'
        self.author_page_type = 'html'
        self.article_page_type = 'html'

        # On Engadget's XML, the dc namespace has https over http
        self.nsmap = {'dc': 'https://purl.org/dc/elements/1.1/'}

        super(Engadget, self).__init__(self.outlet_name)

    
    def get_authors_page(self, author_name):
        """This method provides the author's profile url."""
        return 'http://www.engadget.com/about/editors/' + slugify(author_name)

    
    def extract_articles(self, parsed_xml):
        """
        This method formats Engadget's articles, categories and authors to
        store them in DB; its return should be a list of dictionaries in the
        form given in utils' function `create_article`.
        """

        # Iterates over every item (article) in xml
        for item in parsed_xml.xpath("//item"):

            article = {}
            

            article['title'] = self.get_text_or_attr(item, 'title')


            # The article's categories must be always a list, even if it has
            # only one element.
            categories = self.get_text_or_attr(item, 'category')
            
            if type(categories) == str:
                categories = [categories]

            article['categories'] = categories


            url = self.get_text_or_attr(item, 'link')
            article['url'] = self.remove_query(url)


            # If article's URL is already stored, don't parse it again
            if Article.objects.filter(url = article['url']).count() > 0:
                continue


            # It is interesting to have the publication date as a `dateutil`
            # object, so we can do whatever manipulation we want.
            pub_date = self.get_text_or_attr(item, 'pubDate')
            try:
                article['date'] = dateutil.parser.parse(pub_date)
            except:
                article['date'] = ''


            # Get the author attribute and tries to fetch informations about
            # him/her. An article can have more than one author
            author_names = self.get_text_or_attr(item, 'dc:creator')

            if type(author_names) == str:
                author_names = [author_names]

            article['authors'] = []

            for i in range(len(author_names)):
                self.article_url = article['url']
                article['authors'] += [self.get_author(author_names[i], i)]
            

            # Gets the article's description and strip all html tags from it
            content_thumb = self.get_text_or_attr(item, 'description')
            content = self.clear_text(content_thumb).strip()
            article['content'] = content


            # Tries to find the article's thumbnail url
            thumb = content_thumb.split('<img src="')
            if len(thumb) > 1:
                thumb = thumb[1].split('"')[0]
                thumb = re.findall('storage[^(&|")]{1,}', thumb)
                if thumb:
                    thumb = urllib.parse.unquote(thumb[0])
                    article['thumb'] = 'https://s.aolcdn.com/hss/' + thumb


            yield article


    def extract_twitter(self, parsed_html, author_idx = 0):
        """
        This method extract the twitter username following the author's name
        from an article page.
        """

        twitter_xpath = 'meta[@name="twitter:creator"]'
        handle = self.get_text_or_attr(parsed_html, twitter_xpath, 'content')

        if type(handle) == str and len(handle) > 1:
            return 'https://twitter.com/' + handle[1:]


    def extract_author(self, parsed, author_idx = 0):
        """
        This method extract all important informations about an author. These
        informations can be found by its xpath.
        """

        author = {}


        # Find twitter link
        links = self.get_text_or_attr(parsed, 'div/span/a', 'href')

        for link in links:
            if 'twitter.com' in link:
                author['twitter'] = link


        # Get description text provided by the author
        xpath = './/div[@class="t-d3"]'
        items = parsed.xpath(xpath)
        author['about'] = self.clear_text(items)


        # Get Engadget url profile
        og_url = 'meta[@property="og:url"]'
        author['profile'] = self.get_text_or_attr(parsed, og_url, 'content')


        # Get his/her avatar url
        twitter_image = 'meta[@name="twitter:image"]'
        avatar = self.get_text_or_attr(parsed, twitter_image, 'content')

        if avatar:
            avatar = 'https' + avatar.split('https')[-1]
            author['avatar'] = avatar


        # Check the article's page for his/her twitter if there is an
        # extract_twitter method.
        if not 'twitter' in author:
            parsed = self.parse(self.article_url, self.article_page_type)
            author['twitter'] = self.extract_twitter(parsed, author_idx)


        return author