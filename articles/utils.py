from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify, title
from .models import Author, Category, Outlet, Article

def check_data(data):
    """
    This function checks the data integrity of the `create_article` function
    input. There are some required parameters and some accepted.
    """
    required = {
        'article': ['title', 'url', 'date', 'content', 'authors'],
        'authors': ['name']
    }

    accepted = {
        'article': required['article'] + ['categories', 'thumb'],
        'authors': required['authors'] + ['twitter', 'slug', 'avatar',
            'facebook', 'linkedin', 'about', 'profile', 'website']
    }

    # Check if there is any key not accepted
    msg = {
        'unacceptable': 'There are unacceptable attributes on your request.',
        'required': 'You must provide all required parameters to add an article.'
    }

    # Check first level dictionary keys
    req = required['article'][::]
    for key in data:
        if key not in accepted['article']:
            raise ValueError(msg['unacceptable'])

        if key in required['article']:
            req.remove(key)

    if len(req) > 0:
        raise ValueError(msg['required'])

    # Check second level dictionary keys (authors)
    for author in data['authors']:

        req = required['authors'][::]
        for key in author:
            if key not in accepted['authors']:
                raise ValueError(msg['unacceptable'])

            if key in required['authors']:
                req.remove(key)

        if len(req) > 0:
            raise ValueError(msg['required'])

    return True

def create_article(outlet, data):
    """
    This function creates an article with all its attributes such as its author
    and categories. The data will be checked to make sure no unacceptable input
    comes in and every required attribute is met.
    """

    check_data(data)

    # Form a dictionary with all article's information but its `url`, the
    # article's information can be seen as anything whose type is str inside
    # `data`. However, `date` does not live up by this rule, so we add it
    # manually to article_def.
    url = data.pop('url')

    article_def = {key: data[key] for key in data if type(data[key]) == str}
    article_def['date'] = data.pop('date')
    article_def['outlet_id'] = outlet.id

    article, created = Article.objects.get_or_create(
        url = url,
        defaults = article_def
    )

    # Store non existing authors and assign them to the article
    for author_info in data['authors']:
        # Form a dictionary with all author's information but his/her name
        author_def = {k: author_info[k] for k in author_info if k != 'name'}

        author, created = Author.objects.get_or_create(
            name = author_info['name'],
            outlet_id = outlet.id,
            defaults = author_def
        )

        article.authors.add(author)

    # Store non existing categories and assign them to the article
    data['categories'] = data['categories']

    for cat_name in data['categories']:
        category, created = Category.objects.get_or_create(
            slug = slugify(cat_name),
            defaults = {
                'name': title(cat_name)
            }
        )

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