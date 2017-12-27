import os
from mock import patch
from articles.scrapers.scraper import WebScraper


def get_file(file_name):
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, 'files/' + file_name)
    return open(file_path, encoding='utf8').read().encode('utf8')


@patch('requests.get')
def parse_mocked(file, type, mock_get):
    if type == 'json':
        mock_get.return_value.text = get_file(file)
    else:
        mock_get.return_value.content = get_file(file)
    return WebScraper.parse('', type)