import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
BASE_URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2014/'
BASE_ENCODING = 'gb2312'

PROVINCE_SELECTOR = '.provincetr td a'
CITY_SELECTOR = '.citytr'
COUNTRY_SELECTOR = '.countytr'
TOWN_SELECTOR = '.towntr'
VILLAGE_SELECTOR = '.villagetr'


def get_doc(url):
    '''返回url的BeautifulSoup对象'''
    headers = {'user-agent': USER_AGENT}
    r = requests.get(url, headers=headers)
    r.encoding = BASE_ENCODING;
    return BeautifulSoup(r.text, 'html.parser')


def get_provinces(tags):
    '''从标签返回所有省份信息'''
    province_arr = []
    for tag in tags:
        province_arr.append({'name': tag.contents[0], 'link': concat_url(BASE_URL, tag.get('href'))})
    # 保存数据库
    get_cities(province_arr)


def get_last_index_of(string, mark):
    '''返回mark在string中最后一次出现的位置, 如果没找到, 返回-1, mark为单字符串...'''
    index = -1
    for i in range(len(string[::-1])):
        if string[::-1][i] == mark:
            return len(string) - i - 1
    return index

def concat_url(abs_url, rela_url):
    '''组合url, 因为rela_url是个相对地址'''
    return abs_url[0:(get_last_index_of(abs_url, '/') + 1)] + rela_url

def get_cities(province_arr):
    '''得到城市'''
    for province in province_arr:
        soup = get_doc(province['link'])
        city_arr = []
        for tag in soup.select(CITY_SELECTOR):
            sub_tag = tag.select('td > a')
            city_arr.append({'code': sub_tag[0].contents[0], 'name': sub_tag[1].contents[0], 'link': concat_url(province['link'], sub_tag[0].get('href'))})
        get_countries(city_arr)
    # 保存数据库


def get_countries(city_arr):
    '''得到市辖区'''
    for city in city_arr:
        soup = get_doc(city['link'])
        country_arr = []
        for tag in soup.select(COUNTRY_SELECTOR):
            sub_tag = tag.select('td > a')
            if len(sub_tag) > 0:
                country_arr.append({'code': sub_tag[0].contents[0], 'name': sub_tag[1].contents[0], 'link': concat_url(city['link'], sub_tag[0].get('href'))})
        get_towns(country_arr)
    # 保存数据库


def get_towns(country_arr):
    '''得到镇'''
    for country in country_arr:
        soup = get_doc(country['link'])
        town_arr = []
        for tag in soup.select(TOWN_SELECTOR):
            sub_tag = tag.select('td > a')
            if len(sub_tag) > 0:
                town_arr.append({'code': sub_tag[0].contents[0], 'name': sub_tag[1].contents[0], 'link': concat_url(country['link'], sub_tag[0].get('href'))})
        get_villages(town_arr)


def get_villages(town_arr):
    '''得到居委会'''
    for town in town_arr:
        soup = get_doc(town['link'])
        village_arr = []
        for tag in soup.select(VILLAGE_SELECTOR):
            sub_tag = tag.select('td')
            if len(sub_tag) > 0:
                village_arr.append({'code': sub_tag[0].contents[0], 'class': sub_tag[1].contents[0], 'name': sub_tag[2].contents[0]})
        print(village_arr)


if __name__ == '__main__':
    soup = get_doc(BASE_URL)
    get_provinces(soup.select(PROVINCE_SELECTOR))
