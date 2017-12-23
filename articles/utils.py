from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from .models import Author, Category, Outlet, Article

def create_article(outlet, data):
    """
    This function creates an article with all its attributes such as
    its author and categories.

    Args:
        outlet:  an Outlet object to create/find the author
        data: a dictionary with the article's attributes, with the
              following keys:
               - [required] title
               - [required] url
               - [required] date
               - [optional] thumb
               - [required] content
               - [required*] author
                    - [required] name
                    - [optional] slug
                    - [optional] profile
                    - [optional] twitter
                    - [optional] linkedin
                    - [optional] facebook
                    - [optional] website
                    - [optional] avatar
                    - [optional] about
               - [optional] categories (it's a list with categories' names)
    """

    required = ['title', 'url', 'date', 'content', 'author', 'author.name']
    accepted = required + ['thumb', 'categories', 'author.slug', 'author.profile',
                    'author.twitter', 'author.linkedin', 'author.facebook',
                    'author.website', 'author.avatar', 'author.about']

    # Get input keys with dot notation
    keys = []
    for key in data:
        keys += [key]
        if type(data[key]) == dict:
            keys += [key + '.' + subkey for subkey in data[key]]

    # Check if there is any key not accepted
    for key in keys:
        if key in required:
            required.remove(key)
        if key not in accepted:
            raise ValueError('You can\'t use the attribute `' + key + '`.')
    
    # Check if all required keys were provided correctly
    if len(required) != 0:
        raise ValueError('You must provide all required parameters to add an article.')

    if 'categories' in data and type(data['categories']) != list:
        raise ValueError('The categories parameter should be a list, even if it has only one item.')

    # Form a dictionary with all author's information but his/her name
    author_defaults = {key: data['author'][key] for key in data['author'] if key != 'name'}

    author, created = Author.objects.get_or_create(
        name = data['author']['name'],
        outlet_id = outlet.id,
        defaults = author_defaults
    )

    # Form a dictionary with all article's information but its `url`, the article's
    # information can be seen as anything whose type is str inside `data`. However,
    # `date` does not live up by this rule, so we add it manually to article_defaults.
    url = data.pop('url')
    article_defaults = {key: data[key] for key in data if type(data[key]) == str}
    article_defaults['date'] = data.pop('date')
    article_defaults['author_id'] = author.id
    article_defaults['outlet_id'] = outlet.id

    article, created = Article.objects.get_or_create(
        url = url,
        defaults = article_defaults
    )

    for cat_name in data['categories']:
        category, created = Category.objects.get_or_create(
            slug = slugify(cat_name),
            defaults = {
                'name': cat_name
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