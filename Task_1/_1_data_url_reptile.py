import json
import os
import sys

import requests
from requests_html import HTMLSession
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from db import init_db_data

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
proxies = {
    "http": "socks5h://127.0.0.1:1080", "https": "socks5h://127.0.0.1:1080"
}


def print_schedule(i):
    sys.stdout.write('\r' + str(i))
    sys.stdout.flush()


class RedditDoc(object):
    """
    爬取每个主题下的帖子
    """

    def __init__(self, www_url, max_page=60):
        self.www_url = www_url
        self.session = HTMLSession()
        self.url_list = []
        self.max_page = max_page
        self.i = 0
        self.save_number = 0

    def run(self):
        self.get_url_list(self.www_url)
        return self.save_number

    def save_result(self):
        self.save_number = self.save_number + len(self.url_list)
        with open('../data/reddit_url_list.txt', "a", encoding='utf-8') as file:  # ”w"代表着每次运行都覆盖内容
            for url in self.url_list:
                file.write(url + "\n")
            file.close()
        self.url_list.clear()

    def get_url_list(self, www_url):
        print_schedule(self.save_number)
        res = self.session.get(www_url, headers=headers, verify=False, proxies=proxies)
        res.encoding = 'utf-8'
        html = res.html
        div_list = html.xpath('//*[contains(@class,"thing") and not (contains(@class,"promotedlink"))]')
        for div in div_list:
            url = div.xpath('//@href', first=True)
            if url and "http" not in url:
                self.url_list.append(url)
        if self.i % 10 == 0:  # 每10页面保存一次
            self.save_result()
        self.i += 1
        res.close()
        self.session.close()
        if self.i < self.max_page:
            div_next_button = html.xpath('//*[@class="next-button"]', first=True)
            if div_next_button:
                self.get_url_list(div_next_button.xpath('//a/@href', first=True))
            else:
                self.save_result()


class RedditData(object):
    """
    数据收集爬虫
    """

    def __init__(self, max_page=5):
        self.max_page = max_page
        self.page = 0
        self.save_number = 0
        # 每个主题下的固定分类
        self.type_list = ["", "new/", "rising/", "controversial/", "top/", "gilded/"]
        if os.path.isfile('../data/theme_urls.json'):
            with open('../data/theme_urls.json', 'r', encoding='utf8') as file:
                self.theme_url_list = json.load(file)
        else:
            self.theme_url_list = []

    def run(self):
        # https://old.reddit.com/subreddits
        self.run_theme("https://old.reddit.com/subreddits")

    def save_result(self):
        with open('../data/theme_urls.json', 'w', encoding='utf-8') as file:
            json.dump(self.theme_url_list, file, ensure_ascii=False)
            file.close()

    def run_theme(self, url):
        """
        爬取主题分类
        """
        session = HTMLSession()
        res = session.get(url, headers=headers, verify=False,
                          proxies=proxies)  # proxies=proxies
        res.encoding = 'utf-8'
        html = res.html
        # 获取本页面所有主题div
        div_list = html.xpath('//*[contains(@class,"thing")]')
        for div in div_list:
            # 提取主题链接
            url = div.xpath('//div[2]/p/a/@href', first=True)
            if url not in self.theme_url_list:
                self.theme_url_list.append(url)
                for t in self.type_list:
                    doc_url = url + t
                    print(doc_url, "已经保存:{}".format(self.save_number))
                    reptile = RedditDoc(doc_url)
                    self.save_number = self.save_number + reptile.run()
            # 抓取主题下面的帖子
        self.page += 1
        self.save_result()
        if self.page < self.max_page:
            div_next_button = html.xpath('//*[@class="next-button"]', first=True)
            if div_next_button:
                self.run_theme(div_next_button.xpath('//a/@href', first=True))


def delete_repeat_url():
    """
    删除重复url
    """
    with open("../data/reddit_url_list.txt", "r", encoding='utf-8') as f:
        data_list = f.readlines()
        data_list = list(set(data_list))
        with open('../data/valid_url_list.txt', "w", encoding='utf-8') as file:
            for url in data_list:
                file.write(url[3:])
            file.close()
        f.close()


if __name__ == '__main__':
    """
    爬取贴吧连接
    """
    # reddit_data = RedditData()
    # reddit_data.run()
    # 删除重复url
    delete_repeat_url()
    # 把有效链接插入到MongoDB
    init_db_data()
