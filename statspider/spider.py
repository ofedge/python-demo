import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
BASE_URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2014/index.html'
BASE_ENCODING = 'gb2312'


def get_html(url):
    headers = {'user-agent': USER_AGENT}
    r = requests.get(url, headers=headers)
    r.encoding = BASE_ENCODING;
    return r.text


def getDoc(html_text):
    return BeautifulSoup(html_text, 'html.parser')


if __name__ == '__main__':
    r = getDoc(get_html(BASE_URL))
