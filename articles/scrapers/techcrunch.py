from django.template.defaultfilters import slugify
from articles.scrapers.scraper import WebScraper
from articles.utils import get_text_or_attr, remove_query
import re, dateutil.parser

class TechCrunch(WebScraper):
    """
    This class provides the required methods to scrape an article from
    TechCrunch outlet.
    """
    def __init__(self):
        # Some initial parameters for scraping articles and authors
        self.outlet_slug = 'techcrunch'
        self.feed_url = 'http://feeds.feedburner.com/TechCrunch/'
        self.feed_type = 'xml'
        self.author_page_type = 'html'
        self.article_page_type = 'html'

        super(TechCrunch, self).__init__(self.outlet_slug)

    def get_authors_page(self, author_name):
        """This method provides the author's profile url."""
        return 'http://techcrunch.com/author/' + slugify(author_name)

    def extract_articles(self, parsed_xml):
        """
        This method formats TechCrunch's articles, categories and authors to
        store them in DB; its return should be a list of dictionaries in the
        form given in utils' function `create_article`.
        """
        articles = []

        # Iterates over every item (article) in xml
        for item in parsed_xml.xpath("//item"):
            article = {}
            
            article['title'] = get_text_or_attr(item, 'title')
            article['categories'] = get_text_or_attr(item, 'category')

            url = get_text_or_attr(item, 'feedburner:origLink')
            article['url'] = remove_query(url)

            # It is interesting to have the publication date as a `dateutil`
            # object, so we can do whatever manipulation we want.
            pub_date = get_text_or_attr(item, 'pubDate')
            try:
                article['date'] = dateutil.parser.parse(pub_date)
            except:
                article['date'] = ''

            # Get the author attribute and tries to fetch informations about
            # him/her. An article can have more than one author; on techcrunch's
            # feed, they are separated by a comma.
            author_names = get_text_or_attr(item, 'dc:creator').split(',')
            article['authors'] = []
            for author in author_names:
                article['authors'] + [self.get_author(author, article['url'])]
            
            # Tries to find the article's thumbnail url
            thumb = get_text_or_attr(item, 'media:thumbnail', 'url')
            if thumb and thumb[0]:
                article['thumb'] = remove_query(thumb[0])

            # Gets the article's description and strip all html tags from it
            content = get_text_or_attr(item, 'description')
            content = re.compile(r'<[^>]+>').sub('', content).strip()
            content = content.strip(' Read More').strip('&nbsp;').strip()

            article['content'] = content

            articles += [article]

        return articles

    def extract_twitter(self, parsed_html, author_name = ''):
        """
        This method extract the twitter username following the author's name
        from an article page.
        """
        meta = parsed_html.xpath("/html/head/meta[@name='sailthru.author']")

        # Regex to match twitter usernames
        regex = '(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)'

        if meta:
            content = meta[0].get('content')
            found, twitter = None, None
            
            for author in content.split('/span')[:-1]:
                if author_name in author or author_name == '':
                    found = author
                    twitter = re.findall(regex, author)

            if found and twitter:
                return 'https://twitter.com/' + twitter[0]

        return ''

    def extract_author(self, parsed_html):
        """
        This method extract all important informations about an author. These
        informations can be found by its xpath.
        
        A simple way to find the xpath of a given element is using the browser's
        inspection mode. Chrome has a feature of copying the inspected element's
        xpath.
        """

        author = {}

        # Find all links with this xpath and tries to classify them
        links = []
        xpath = '/html/body/div[4]/div[2]/div[1]/div/div[1]/div[1]/ul/li/a'

        for a in parsed_html.xpath(xpath):
            links += [a.get('href')]
        
        for social in self.classify_links(links):
            author[social[0]] = social[1]

        # Get description text provided by the author
        author['about'] = ''
        xpath = '/html/body/div[4]/div[2]/div[1]/div/div[1]/div[2]/p'

        for p in parsed_html.xpath(xpath):
            author['about'] += self.html_to_string(p)

        # Get Crunchbase url profile
        xpath = '/html/body/div[4]/div[2]/div[1]/div/div[1]/div[2]/a'
        profile = parsed_html.xpath(xpath)

        if profile:
            author['profile'] = profile[0].get('href')

        # Get his/her avatar url
        xpath = '/html/body/div[4]/div[2]/div[1]/div/div[1]/div[1]/img'
        avatar = parsed_html.xpath(xpath)

        if avatar:
            author['avatar'] = avatar[0].get('src')

        return author