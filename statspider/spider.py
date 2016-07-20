import requests
import logging
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
BASE_URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2014/'
BASE_ENCODING = 'gb2312'

PROVINCE_SELECTOR = '.provincetr td a'
CITY_SELECTOR = '.citytr'
COUNTRY_SELECTOR = '.countytr'
TOWN_SELECTOR = '.towntr'
VILLAGE_SELECTOR = '.villagetr'

SQLITE_URI = 'sqlite:///db'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='spider.log',
                    filemode='a')


def get_doc(url):
    '''返回url的BeautifulSoup对象'''
    headers = {'user-agent': USER_AGENT}
    r = requests.get(url, headers=headers)
    r.encoding = BASE_ENCODING;
    return BeautifulSoup(r.text, 'html.parser')


def get_provinces(tags, session):
    '''从标签返回所有省份信息'''
    logging.info('starting...')
    province_arr = []
    for tag in tags:
        province = Province(name=tag.contents[0])
        save_entry(session, province)
        logging.info('province:' + province.name + 'saved')
        province_arr.append({'id': province.id, 'link': concat_url(BASE_URL, tag.get('href'))})
    get_cities(province_arr, session)


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

def get_cities(province_arr, session):
    '''得到城市'''
    for province in province_arr:
        soup = get_doc(province['link'])
        city_arr = []
        for tag in soup.select(CITY_SELECTOR):
            sub_tag = tag.select('td > a')
            city = City(name=sub_tag[1].contents[0], code=sub_tag[0].contents[0], province_id=province['id'])
            save_entry(session, city)
            logging.info('city:' + city.name + 'saved')
            city_arr.append({'id': city.id, 'link': concat_url(province['link'], sub_tag[0].get('href'))})
        get_countries(city_arr, session)


def get_countries(city_arr, session):
    '''得到市辖区'''
    for city in city_arr:
        soup = get_doc(city['link'])
        country_arr = []
        for tag in soup.select(COUNTRY_SELECTOR):
            sub_tag = tag.select('td > a')
            if len(sub_tag) > 0:
                country = Country(name=sub_tag[1].contents[0], code=sub_tag[0].contents[0], city_id=city['id'])
                save_entry(session, country)
                logging.info('country:' + country.name + 'saved')
                country_arr.append({'id': country.id, 'link': concat_url(city['link'], sub_tag[0].get('href'))})
        get_towns(country_arr, session)


def get_towns(country_arr, session):
    '''得到镇'''
    for country in country_arr:
        soup = get_doc(country['link'])
        town_arr = []
        for tag in soup.select(TOWN_SELECTOR):
            sub_tag = tag.select('td > a')
            if len(sub_tag) > 0:
                town = Town(name=sub_tag[1].contents[0], code=sub_tag[0].contents[0], country_id=country['id'])
                save_entry(session, town)
                logging.info('town:' + town.name + 'saved')
                town_arr.append({'id': town.id, 'link': concat_url(country['link'], sub_tag[0].get('href'))})
        get_villages(town_arr, session)


def get_villages(town_arr, session):
    '''得到居委会'''
    for town in town_arr:
        soup = get_doc(town['link'])
        village_arr = []
        for tag in soup.select(VILLAGE_SELECTOR):
            sub_tag = tag.select('td')
            if len(sub_tag) > 0:
                village = Village(name=sub_tag[2].contents[0], code=sub_tag[0].contents[0], type=sub_tag[1].contents[0], town_id=town['id'])
                save_entry(session, village)
                logging.info('village' + village.name + 'saved')
    logging.info('all done')


def get_session():
    '''获取sqlalchemy的session'''
    engine = create_engine(SQLITE_URI)
    Session = sessionmaker(bind=engine)
    return Session();


def save_entry(session, entry):
    '''保存并提交数据, 不提交不给id!!!'''
    session.add(entry)
    session.commit()


Base = declarative_base()


class Province(Base):
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return '<Province(id=%s, name=%s)>' % (self.id, self.name)


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    province_id = Column(Integer)

    def __repr__(self):
        return '<City(id=%s, name=%s, code=%s, province_id=%s)>' % (self.id, self.name, self.code, self.province_id)


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    city_id = Column(Integer)

    def __repr__(self):
        return '<Country(id=%s, name=%s, code=%s, province_id=%s)>' % (self.id, self.name, self.code, self.city_id)


class Town(Base):
    __tablename__ = 'town'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    country_id = Column(Integer)

    def __repr__(self):
        return '<Town(id=%s, name=%s, code=%s, province_id=%s)>' % (self.id, self.name, self.code, self.country_id)


class Village(Base):
    __tablename__ = 'village'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    type = Column(String)
    town_id = Column(Integer)

    def __repr__(self):
        return '<Village(id=%s, name=%s, code=%s, type=%s, town_id=%s)>' % (self.id, self.name, self.code, self.type, self.town_id)


if __name__ == '__main__':
    soup = get_doc(BASE_URL)
    session = get_session()
    get_provinces(soup.select(PROVINCE_SELECTOR), session)
