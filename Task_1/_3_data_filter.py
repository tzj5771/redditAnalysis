import codecs
import csv
import math
import os
import re

from db import get_list_by_status
from nltk.corpus import stopwords

punctuation = r"""!"#$%&'()*+,？-./:;<=>?@[\]^_`{|}~！•⚠💎🙌🏽💎🍆😂s❤🤦🏼‍♂🤗💖–🦍💽1234567890⠄⠄⠄⣿"""
stopwords_english = stopwords.words('english')
with open('../data/stop_english.txt', 'r', encoding='utf-8') as fp:
    for word in fp.readlines():
        stopwords_english.append(word.strip())
for w in ['!', ',', '.', '?', '-s', '-ly', '</s>', 's', 'div']:
    stopwords_english.append(w)

html_div = ["div clacolinput maxlength namecart typetextdiv", 'panmonthpaninput maxlength namemonth typetext',
            'pancard numberpandiv clarow boxrow', 'panyearpaninput maxlength nameyear typetext',
            'li clawcpaymentmethod paymentmethodpaypal', 'pannamepaninput namename typetext', 'div clacol',
            'clarow boxrow', 'div',
            'pancvvpaninput maxlength namecvv typepaword', 'label forcvv', 'label formonth']


def filter_result(size=10000, skip=0):
    data = get_list_by_status(1, size, skip)
    data_valid_data = []
    for d in data:
        comment = d['comment'].lower()
        if len(comment) > 2000:
            title = d['title'].translate(str.maketrans(' ', ' ', punctuation)).lower()  # 去除标点符号
            if len(d['comment']) > 10000:
                comment = comment[:10000]
            comment = comment.translate(str.maketrans(' ', ' ', punctuation))  # 去除标点符号
            comment = re.sub(r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b", ' ', comment, flags=re.MULTILINE)
            comment = re.sub(' +', ' ', comment)
            filtered = [w.lower() for w in comment.split(" ") if (w.lower() not in stopwords_english)]
            label = d['url'].split("/")[0]
            filtered = " ".join(filtered)
            for w in html_div:
                filtered = filtered.replace(w, '')
            filtered = re.sub(' +', ' ', filtered)
            data_valid_data.append({
                "label": label.lower(),
                "title": title,
                "comment": filtered,
            })
    save_test_result(data_valid_data)


def save_test_result(data_list):
    """
    保存预测结果
    """
    csv_file = codecs.open('../data/analysis_data.csv', 'a+', encoding='utf-8')
    writer = csv.writer(csv_file)
    for index, d in enumerate(data_list):
        writer.writerow((d['label'], d['title'], len(d['title']), d['comment'], len(d['comment'])))
    csv_file.close()


def data_handle(size, is_remove_svg=False):
    if is_remove_svg and os.path.exists("../data/analysis_data.csv"):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove("../data/analysis_data.csv")
    page_size = 5000
    if size > page_size:
        count = math.ceil(size / page_size)
        for i in range(count):
            print(page_size, i * page_size)
            filter_result(page_size, i * page_size)
    else:
        filter_result(size, 0)


if __name__ == '__main__':
    # # 过滤 特殊符号 并且保存
    data_handle(30000, True)
    # import nltk
    # nltk.download() #
