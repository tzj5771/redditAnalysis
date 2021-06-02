import abc
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix

from sklearn.model_selection import train_test_split


class DataLoadHandle(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = pd.read_csv('../data/analysis_data.csv')
        print("--------Data length:{}--------".format(len(self.data)))
        self.data.columns = ['label', 'title', "title_length", 'comment', "comment_length"]
        # # 分割训练集与测试集
        xtrain, xtest, ytrain, ytest = train_test_split(self.data, range(self.data.shape[0]), test_size=0.75,
                                                        random_state=5)
        self.train_documents, self.train_labels = self.load_data(xtrain)
        self.test_documents, self.test_labels = self.load_data(xtest)

    def load_data(self, data_list):
        documents = []
        labels = []
        for label, title, comment in zip(data_list['label'], data_list['title'], data_list['comment']):
            labels.append(label)
            documents.append("{} {}".format(title, comment))
        return documents, labels

    def assess(self, predicted_labels, is_print=True):
        acc = metrics.accuracy_score(self.test_labels, predicted_labels)
        # precision = metrics.precision_score(self.test_labels, predicted_labels, average='micro')
        # recall = metrics.recall_score(self.test_labels, predicted_labels,average='micro')
        # f1 = 2 * (precision * recall) / (precision + recall)
        # c_m = confusion_matrix(self.test_labels, predicted_labels)
        if is_print:
            print("--------F1 Score ratio--------".format(len(self.data)))
            c_r = metrics.classification_report(self.test_labels, predicted_labels)
            lines = c_r.split("\n")
            print(lines[0])
            print(lines[-3])
            print(lines[-2])
            print(lines[-31])
        print("--------ACC--------")
        print(acc)
        # return acc

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def run(self):
        pass
