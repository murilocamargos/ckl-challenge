from django.template.defaultfilters import slugify

from articles.scrapers.scraper import WebScraper
from articles.models import Article

class TechCrunch(WebScraper):
    """
    This class provides the required methods to scrape an article from
    TechCrunch outlet. Fetching an article from TechCrunch follows the above
    steps:

    1) Download the TechCrunch XML feed at `feed_url`

    2) Go through every item on this feed and for each one extract informations
       such as title, url, pub_date, categories, content, thumb and authors.

    3) Luckily, all the article's information can be fetched from this source;
       but not the author's. Step 3 is called inside step's 2 method to get
       information about the author(s).

    4) The author profile page is given by slugification at `get_authors_page`.
       This page is parsed and his/her information may or may not be there.
       Generally it is, but if it's not, it can be that just slugifying his/her
       name and appending to a prefix is not good enough; so we go back to the
       article's page to try to find the authors.

    5) Generally at the article's page we can find the author's name, profile
       and twitter handle. So we go back to the found profile page to try to
       find more information such as their avatar, other social medias and text
       written by them.

    """

    def __init__(self):
        # Some initial parameters for scraping articles and authors
        super(TechCrunch, self).__init__('TechCrunch')

        self.feed_url = 'http://feeds.feedburner.com/TechCrunch/'
        self.feed_type = 'xml'
        self.author_page_type = 'html'
        self.article_page_type = 'html'
        self.article_url = None


    @staticmethod
    def get_authors_page(author_name):
        """This method provides the author's profile url."""
        return 'http://techcrunch.com/author/' + slugify(author_name)


    def extract_articles(self, parsed_xml):
        """
        This method formats TechCrunch's articles, categories and authors to
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

            if isinstance(categories, str):
                categories = [categories]

            article['categories'] = categories


            url = self.get_text_or_attr(item, 'feedburner:origLink')
            article['url'] = self.remove_query(url)

            self.article_url = article['url']


            # If article's URL is already stored, don't parse it again
            if Article.objects.filter(url=article['url']).count() > 0:
                continue


            # It is interesting to have the publication date as a `dateutil`
            # object, so we can do whatever manipulation we want.
            pub_date = self.get_text_or_attr(item, 'pubDate')
            article['date'] = self.parse_datetime_passing_errors(pub_date)


            # Get the author attribute and tries to fetch informations about
            # him/her. An article can have more than one author; on techcrunch's
            # feed, they are separated by a comma.
            author_names = self.get_text_or_attr(item, 'dc:creator').split(',')
            article['authors'] = []

            for i, name in enumerate(author_names):
                article['authors'] += [self.get_author(name, i)]


            # Tries to find the article's thumbnail url
            thumb = self.get_text_or_attr(item, 'media:thumbnail', 'url')
            if thumb and thumb[0]:
                article['thumb'] = self.remove_query(thumb[0])


            # Gets the article's description and strip all html tags from it
            content = self.clear_text(item.xpath('description'))
            content = content.strip(' Read More').strip('&nbsp;').strip()


            article['content'] = content


            yield article


    def extract_author_from_page(self, parsed, author_idx=0):
        """
        This method goes back in the article's page and tries to find at the
        author's profile page and twitter handle. This happens because there
        are times when the XML feed gives a name that can't be correctly
        transformed in the author's page url by slugification.
        """

        author = {}

        author_url = parsed.xpath('//a[@rel="author"]')
        if author_url and len(author_url) > author_idx:
            author['profile'] = 'https://techcrunch.com'
            author['profile'] += author_url[author_idx].get('href')


        # Find the twitter handle associated with the i-th author
        twitter_handle = parsed.xpath('//span[@class="twitter-handle"]/a')
        if twitter_handle and len(twitter_handle) > author_idx:
            author['twitter'] = twitter_handle[author_idx].get('href')


        # Parse the new author's page and send it back to `extract_author`.
        # In case the profile page found on article's page does not exist as
        # well, this will be going back and forth on an infinite basis. To exit
        # this loop, we added a flag on the author dict.
        author['flag'] = 'exit'

        parsed = self.parse(author['profile'], self.author_page_type)

        return self.extract_author(parsed, author_idx, author)


    def extract_author(self, parsed_html, author_idx=0, author=None):
        """
        This method extract all important informations about an author. These
        informations can be found by its xpath.

        A simple way to find the xpath of a given element is using the browser's
        inspection mode. Chrome has a feature of copying the inspected element's
        xpath.
        """

        if not author:
            author = {}


        # Find all links with this xpath and tries to classify them
        links = []
        xpath = '//div[@class="profile cf"]/div/ul/li/a'

        for url in parsed_html.xpath(xpath):
            links += [url.get('href')]

        for social in self.classify_links(links):
            author[social[0]] = social[1]


        # Get description text provided by the author
        xpath = '//div[contains(@class, "profile-text")]/p'
        items = parsed_html.xpath(xpath)
        author['about'] = self.clear_text(items)


        # Get Crunchbase url profile
        xpath = '//div[contains(@class, "profile-text")]/a'
        website = parsed_html.xpath(xpath)

        if website:
            author['website'] = website[0].get('href')


        # Get his/her avatar url
        xpath = '//div[@class="profile cf"]/div/img'
        avatar = parsed_html.xpath(xpath)

        if avatar:
            author['avatar'] = avatar[0].get('src')


        # Tries to get the author's profile url
        xpath = 'meta[@property="og:url"]'
        author['profile'] = self.get_text_or_attr(
            parsed_html, xpath, 'content'
        )


        # If the author cannot be fetched from his generated url, we have to
        # check the article's page in order to find him/her.

        if 'twitter' not in author and 'flag' not in author:

            parsed = self.parse(self.article_url, self.article_page_type)
            return self.extract_author_from_page(parsed, author_idx)


        if 'flag' in author:
            del author['flag']


        return author
