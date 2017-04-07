from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests


AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = 'b247194c3e4e426ab333b333206d8fe0'  # Your app_id here

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAADQg7xAAQuoEqzv-u2GE5btQj0Lvs5q3I'  # Your token here


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token): # зачем нужна эта функция/метод?
        self.token = token     # что такое __init__ и self зачем эти параметры?

    def get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'python3'
        }

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def get_visits_count(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(url, params=params, headers=headers)
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count

    def get_pageviews_count(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(url, params=params, headers=headers)
        pageviews_count = response.json()['data'][0]['metrics'][0]
        return pageviews_count

    def get_users_count(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(url, params=params, headers=headers)
        users_count = response.json()['data'][0]['metrics'][0]
        return users_count

def get_my_counter_mertic():
    metrika = YandexMetrika(TOKEN)
    for counter in metrika.counter_list:
        print("Количество визитов: {}" .format(metrika.get_visits_count(counter)))
        print("Количество просмотров: {}".format(metrika.get_pageviews_count(counter)))
        print("Количество посетителей: {}".format(metrika.get_users_count(counter)))


get_my_counter_mertic()