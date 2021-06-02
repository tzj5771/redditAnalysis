import math

import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics, linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from Task_3.data_load_handle import DataLoadHandle


class RegressionAnalysis(DataLoadHandle):
    def __init__(self):
        super().__init__()

    def nbc(self, data_len):
        if data_len < len(self.data):
            data_handle = self.data[:data_len]
        else:
            data_handle = self.data
        data_handle.columns = ['label', 'title', "title_length", 'comment', "comment_length"]
        # # 分割训练集与测试集
        xtrain, xtest, ytrain, ytest = train_test_split(data_handle, range(data_handle.shape[0]), test_size=0.75,
                                                        random_state=5)
        train_documents, train_labels = self.load_data(xtrain)
        test_documents, test_labels = self.load_data(xtest)
        # 计算矩阵
        tt = TfidfVectorizer(max_df=0.5)
        tf = tt.fit_transform(train_documents)
        # 训练模型
        clf = MultinomialNB(alpha=0.001).fit(tf, train_labels)
        # 模型预测
        test_tf = TfidfVectorizer(max_df=0.5, vocabulary=tt.vocabulary_)
        test_features = test_tf.fit_transform(test_documents)
        predicted_labels = clf.predict(test_features)
        acc = metrics.accuracy_score(test_labels, predicted_labels)
        return acc

    def run(self):
        page_size = 50
        count = math.ceil(500 / page_size)
        x_train = []
        y_train = []
        for i in range(page_size):
            size = (i + 1) * count
            x_train.append(size)
            y_train.append(self.nbc(size))
        model = linear_model.LinearRegression()
        x_train = np.array(x_train).reshape(-1, 1)
        y_train = np.array(y_train).reshape(-1, 1)
        model.fit(x_train, y_train)

        a = model.intercept_
        b = model.coef_
        plt.scatter(x_train, y_train, color='blue', label="train data")
        y_train_pred = model.predict(x_train)
        plt.plot(x_train, y_train_pred, color='black', linewidth=3, label="best line")
        plt.legend(loc=2)
        plt.xlabel("Number of articles")
        plt.ylabel("ACC")
        plt.show()
        # return a,b


if __name__ == '__main__':
    ra = RegressionAnalysis()
    ra.run()
