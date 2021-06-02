import random
import time

from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from db import get_list_by_status, update_t_c_by_id, get_list_by_status_sort, get_valid_list


# function to wait for random time


def random_wait(a=0, b=None):
    if b != None:
        time.sleep(random.randrange(a, b))
    else:
        time.sleep(a)


def generate_code():
    seeds = "1234567890"
    random_num = []
    for i in range(8):
        random_num.append(random.choice(seeds))
    return "".join(random_num)


class RepeatHtml(object):

    def __init__(self, url_list):
        self.url_list = url_list
        self.isLogin = True
        self.driver = None
        self.init_browser()
        self.login()
        if self.isLogin and self.driver:
            for obj in url_list:
                self.open_url(obj)
        if self.driver:
            self.driver.quit()
        # for obj in url_list:
        #     print(obj['url'])
        #     update_comment_by_id(obj['_id'], "cc")

    def init_browser(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        # Configure driver and driver options
        options = Options()
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument("--disable-notifications")
        # driver_path = Path('chromedriver.exe').as_posix()
        # self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        options = Options()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-notifications")
        # options.add_argument('--headless')  # 设置无界面
        # options.add_argument('--no-sandbox')  # root用户下运行代码需添加这一行
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        login_url = 'https://www.reddit.com/login/'
        self.driver.get(login_url)
        random_wait(2, 6)
        account = ["xx", "xxx"]
        try:
            # find the form element
            form = self.driver.find_element_by_class_name('AnimatedForm')
            # enter username
            username = form.find_element_by_id('loginUsername')
            username.clear()
            username.send_keys(account[0])
            # enter password
            password = form.find_element_by_id('loginPassword')
            password.clear()
            password.send_keys(account[1])
            # time.sleep(3)
            # click to login
            button = form.find_element_by_class_name('AnimatedForm__submitButton')
            button.click()
            time.sleep(3)
            print("正在登录")
            self.isLogin = True
        except Exception as e:
            self.isLogin = False
            print('Login issue', e)

    def open_url(self, obj):
        start = time.time()
        self.driver.get("https://www.reddit.com/r/{}".format(obj['url']))
        end = time.time()
        print(end, end - start, obj['_id'])
        # random_wait(1)
        # try:
        #     # scroll down website
        #     page_html = self.driver.find_element_by_tag_name('html')
        #     for i in range(2):
        #         page_html.send_keys(Keys.END)
        #         random_wait(1)
        # except Exception as e:
        #     print('Scrolling issue:', e)
        # try:
        #     # Expand all
        #     div_list = self.driver.find_elements_by_class_name('_2HYsucNpMdUpYlGBMviq8M')
        #     more_btn = []
        #     for btn in div_list:
        #         if "more replies" in str(btn.text):
        #             more_btn.append(btn)
        #             # driver.execute_script("arguments[0].click();", btn)
        #             # time.sleep(1)
        #     if len(more_btn) > 0:
        #         self.driver.execute_script("arguments[0].click();", more_btn[-1])
        #         time.sleep(1)
        # except Exception as e:
        #     print('more replies:', e)
        try:
            content = self.driver.page_source
            tree = html.fromstring(str(content))
            div_title_list = tree.xpath(
                '//*[contains(@class,"_2SdHzo12ISmrC8H86TgSCp") and (contains(@class,"_29WrubtjAcKqzJSPdQqQ4h"))]')
            title = ""
            if len(div_title_list) > 0:
                title_list = div_title_list[0].xpath("//h1/text()")
                if len(title_list) > 0:
                    title = title_list[0]
            div_comment_list = tree.xpath('//*[contains(@class,"_292iotee39Lmt0MkQZ2hPV")]')
            div_element_txt_list = []
            for div in div_comment_list:
                p = div.xpath('//p/text()')
                if p and len(p) > 0:
                    p_txt = "".join(p)
                    div_element_txt_list.append(p_txt)
            update_t_c_by_id(obj['_id'], title, "".join(div_element_txt_list))
            # random_wait(1)
        except Exception as e:
            print('html :', e)


if __name__ == '__main__':
    url_list = get_valid_list()
    repeat_html = RepeatHtml(url_list)
