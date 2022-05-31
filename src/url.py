import requests
from requests.exceptions import ConnectionError


class Page:
    cache = {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    def __init__(self):
        self.base_url = None
        self.destination_url = None
        self.nb_redirect = 0
        self.status_code = 200

    @staticmethod
    def from_url(url):

        if url not in Page.cache.keys():
            page = Page()
            page.base_url = url

            try:
                r = requests.get(url, headers=Page.headers)
                page.destination_url = r.url
                page.nb_redirect = len(r.history)
                page.status_code = r.status_code
            except ConnectionError as e:
                page.destination_url = url
                page.nb_redirect = 0
                page.status_code = 404

            Page.cache[url] = page
        return Page.cache[url]
