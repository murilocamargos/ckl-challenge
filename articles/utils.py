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