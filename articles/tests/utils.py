import os, pickle
from mock import patch
from articles.scrapers.scraper import WebScraper

def open_file(file_name, mode='r', encoding='utf8'):
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, 'files/' + file_name)
    return open(file_path, mode=mode, encoding=encoding)

def get_file(file_name):
    return open_file(file_name).read().encode('utf8')


@patch('twitter.Api.GetUserTimeline')
@patch('requests.get')
def parse_mocked(file, type, mock_get, mock_twitter):
    if type == 'twitter':
        pickle_in = open_file(file, 'rb', None)
        mock_twitter.return_value = pickle.load(pickle_in)
    elif type == 'json':
        mock_get.return_value.text = get_file(file)
    else:
        mock_get.return_value.content = get_file(file)
    return WebScraper.parse('', type)