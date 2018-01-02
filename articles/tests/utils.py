"""
This file brings some utility functions used by tests.
"""

import os
import pickle

from mock import patch

from articles.scrapers.scraper import WebScraper


def open_file(file_name, mode='r', encoding='utf8'):
    """Open file inside tests/files directory with given mode and encoding."""
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, 'files/' + file_name)
    return open(file_path, mode=mode, encoding=encoding)


def get_file(file_name, encoding='utf8'):
    """Reads opened file."""
    return open_file(file_name, encoding=encoding).read().encode(encoding)


@patch('twitter.Api.GetUserTimeline')
@patch('requests.get')
def parse_mocked(file, data_type, mock_get, mock_twitter):
    """Implements a parsing function for mocked data."""
    if data_type == 'twitter':
        pickle_in = open_file(file, 'rb', None)
        mock_twitter.return_value = pickle.load(pickle_in)

    elif data_type == 'json':
        mock_get.return_value.text = get_file(file)

    else:
        mock_get.return_value.content = get_file(file)

    return WebScraper.parse('', data_type)
