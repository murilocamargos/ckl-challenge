import django.template.defaultfilters as filters

from articles.scrapers.scraper import WebScraper
from articles.models import Article


class Mashable(WebScraper):
    """
    This class provides the required methods to scrape an article from Mashable
    outlet. Fetching an article from Mashable follows the above steps:

    1) Get the twitter feed from `mashabletech` account. We could just use
       their XML rss feed, but this contains articles of all categories and we
       want to focus on tech related articles.

    2) Find all links leading to Mashable website; these are the articles'
       pages themselves. We parse these pages looking for article information
       and something that could lead us to the author's profile page.

    3) If we find the author's page, we parse it and store the information.
    """

    def __init__(self):
        # Some initial parameters for scraping articles and authors
        super(Mashable, self).__init__('Mashable')

        self.feed_url = 'mashabletech'
        self.feed_type = 'twitter'
        self.author_page_type = 'html'
        self.article_page_type = 'html'
        self.author_url = None


    def get_authors_page(self, author_name):
        """
        This method provides the author's profile url, the url can be set
        previously at the `author_url` attribute; but it can only be used once.
        """

        if self.author_url:
            # Use and remove `author_url`
            url, self.author_url = self.author_url, None

            return url

        return 'http://mashable.com/author/' + filters.slugify(author_name)


    def article_info(self, parsed):
        """
        All the information needed do add an article can be found in the
        article's page except the author's which will be fetched at another
        page.
        """

        data = {}


        # Gets the title, url and pub_date in the metatags
        data['title'] = self.get_text_or_attr(parsed, \
            'meta[@property="og:title"]', 'content')

        data['url'] = self.remove_query(self.get_text_or_attr(parsed, \
            'meta[@property="og:url"]', 'content'))

        data['date'] = self.get_text_or_attr(parsed, \
            'meta[@property="og:article:published_time"]', 'content')

        data['date'] = self.parse_datetime_passing_errors(data['date'])


        if not data['title'] or not data['url'] or not data['date']:
            return {}


        # Tries to get the author's name
        author_name = self.get_text_or_attr(parsed, 'meta[@name="author"]', \
            'content')


        # If article's URL is already stored, don't parse it again
        if Article.objects.filter(url=data['url']).count() > 0:
            return {}


        # Get the article's thumbnail
        thumb = self.get_text_or_attr(parsed, 'meta[@property="og:image"]', \
            'content')

        if thumb:
            data['thumb'] = thumb


        # Get the article's categories as a list
        cats = self.get_text_or_attr(parsed, 'meta[@name="keywords"]', \
            'content')

        if cats:
            data['categories'] = [filters.title(c) for c in cats.split(', ')]



        # At this point, there is no Mashable article with more than one author
        # we know about. When this case comes up, we need to deal with it here.
        # A for loop should suffice.
        author = {
            'name': author_name
        }

        # Tries to find his/her profile page
        page = self.get_text_or_attr(parsed, 'span[@class="author_name"]/a', \
            'href')

        prefix = 'http://mashable.com'

        # By default, the author's url profile is given by his/her name
        # slugified, but if his page is found at the parsed HTML, use it.
        self.author_url = prefix + '/author/' + filters.slugify(author_name)
        if page:
            self.author_url = prefix + page

        # Set his profile page as the url to be fetched by `get_author`
        author.update(self.get_author(author_name, 0))


        # Add author to the list
        data['authors'] = [author]


        # Get article's content
        items = parsed.xpath('.//section[@class="article-content blueprint"]/p')
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
                date = self.parse_datetime_passing_errors(status.created_at)

                if not date:
                    continue

                article['date'] = date


            yield article


    def extract_author(self, parsed, author_idx=0):
        """
        This method extract all important informations about an author. These
        informations can be found by its xpath.

        A simple way to find the xpath of a given element is using the browser's
        inspection mode. Chrome has a feature of copying the inspected element's
        xpath.
        """

        author = {}

        # Find all links with this xpath and tries to classify them
        links = self.get_text_or_attr(parsed, \
            'div[@class="profile-networks"]/a', 'href')

        if isinstance(links, str):
            links = [links]

        for social in self.classify_links(links):
            author[social[0]] = social[1]


        # Get description text provided by the author
        items = parsed.xpath('.//div[@class="profile-about"]')
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
