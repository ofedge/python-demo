#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
cnki_spider.py

CNKI的下载工具, 前提是你可以免费下载~~

Usage:

python3 cnki_spider.py

'''

import requests, time, os, random
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
BASE_HOST = 'http://www.cnki.com.cn'
BASE_URL = 'http://yuanjian.cnki.com.cn/CJFD/Detail/CJFDResult'
BASE_ENCODING = 'utf-8'


def get_doc(url, param={}):
    '''返回url的BeautifulSoup对象'''
    headers = {'user-agent': USER_AGENT}
    
    r = requests.post(url, headers=headers, data=param)
    r.encoding = BASE_ENCODING;
    return BeautifulSoup(r.text, 'html.parser')


def get_books(soup):
    '''得到12本书的url'''
    book_arr = []
    books = soup.select('#CJFDIssue > div > div > a')
    for book in reversed(books):
        book_arr.append(book.get('href'))
    return book_arr;


def get_contents(book_arr):
    ''' 得到12本书的所有目录下载页'''
    article_dic = {}
    for i in range(len(book_arr)):
        article_dic[i] = []
        soup = get_doc(book_arr[i])
        tags = soup.select('#articleList td a');
        for tag in tags:
            print('name:', tag.contents[0], ', url:', BASE_HOST + tag.get('href'))
            article_dic[i].append({'name': tag.contents[0], 'url': BASE_HOST + tag.get('href')})
    return article_dic


def download_now(article_dic):
    print('任务开始, 一共', len(article_dic), '期')
    for i in range(len(article_dic)):
        foldername = '第' + str(i+1) + '期'
        os.mkdir(foldername)
        print('准备下载', foldername)
        n = 0
        for article in article_dic[i]:
            down_soup = get_doc(article['url'])
            url_tags = down_soup.select('#ty_pdf a')
            for url_tag in url_tags:
                n = n + 1
                print('正在下载第', i+1, '期第', n, '个文件')
                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                           'Accept-Encoding': 'gzip, deflate, sdch',
                           'Accept-Language': 'zh-CN,zh;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
                           'Referer': article['url']}
                re = requests.get(replace_space(url_tag.get('href')), headers=headers)
                with open(foldername+'/'+replace_mark(article['name'])+'.pdf', 'wb') as f:
                    f.write(re.content)
                sleep_time = random.randint(8, 15)
                print('休眠', sleep_time, '秒')
                time.sleep(sleep_time)
        print('第', i+1, '期', n, '个文件已下载完成')


def replace_space(string):
    return string.replace('\n','').replace('\t','').replace(' ','')

def replace_mark(string):
    return replace_space(string).replace('/','_')\
           .replace('\\','_').replace(':','_')\
           .replace('：','_').replace('*','_')\
           .replace('?','_').replace('？','_')\
           .replace('"','_').replace('＂','_')\
           .replace('＂','_').replace('“','_')\
           .replace('”','_').replace('|','_')\
           .replace('<','_').replace('>','_')\
           .replace('《','_').replace('》','_')


if __name__ == '__main__':
    param = {'PYKM': 'XYWM', 'Page': 2, 'Year': ''}
    # 获取根文档
    soup = get_doc(BASE_URL, param)
    # 获取12本书
    book_arr = get_books(soup)
    # 获取12本书所有目录
    article_dic = get_contents(book_arr)
    # 开始下载
    download_now(article_dic)
    
