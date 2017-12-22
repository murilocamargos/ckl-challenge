from django.shortcuts import get_object_or_404
from .models import Author, Category, Outlet, Article

def create_article(outlet, data):
    """
    This function creates an article with all its dependencies, such as,
    its author and categories.

    Args:
        outlet:  an Outlet object to create/find the author
        data: a dictionary with the article's attributes, with the
                 following structure:
                  - title
                  - url
                  - date
                  - thumb
                  - content
                  - author
                    - name
                    - avatar
                  - categories (a list of categories' names)
    """
    if data['date'] == '' or data['title'] == '':
        return None

    author, created = Author.objects.get_or_create(
        name = data['author']['name'],
        outlet_id = outlet.id,
        defaults = {
            'avatar': data['author']['avatar']
        }
    )

    article, created = Article.objects.get_or_create(
        url = data['url'],
        defaults = {
            'title': data['title'],
            'date': data['date'],
            'thumb': data['thumb'],
            'content': data['content'],
            'author_id': author.id,
            'outlet_id': outlet.id
        }
    )

    for cat_name in data['categories']:
        category, created = Category.objects.get_or_create(name = cat_name)
        article.categories.add(category)

    return article

def get_text_or_attr(item, key, attr = None):
    """
    This function returns a string or a list of strings containing
    the text inside or an attribute value of lxml Elements.

    Args:
        item: must be an Element from a lxml parsing.
        key:  it's the name of children tags to find.
        attr: if this is provided, the attribute `attr` will be fetched
              instead of the text.
    """

    # This namespace mapping may change with different outlets
    nsmap = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        'media': 'http://search.yahoo.com/mrss/',
        'feedburner': 'http://rssnamespace.org/feedburner/ext/1.0',
    }

    search = item.xpath('.//' + key, namespaces=nsmap)

    items = []
    if len(search) > 0:
        if attr:
            items = [item.get(attr) for item in search]
        else:
            items = [item.text for item in search]

    # Retrieve item itself if there's only one in the list
    if len(items) == 1:
        return items[0]
    return items

def remove_query(url):
    """This function removes anything after `?` from a string."""
    if type(url) == str:
        return url.split('?')[0]