import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import seaborn as sns
from Task_3.data_load_handle import DataLoadHandle
import warnings

warnings.filterwarnings("ignore")


class NBC(DataLoadHandle):
    def __init__(self):
        super().__init__()

    def run(self):
        # 计算矩阵
        tt = TfidfVectorizer(max_df=0.5)
        tf = tt.fit_transform(self.train_documents)
        # 训练模型
        clf = MultinomialNB(alpha=0.001).fit(tf, self.train_labels)
        print(clf.intercept_)
        # 模型预测
        test_tf = TfidfVectorizer(max_df=0.5, vocabulary=tt.vocabulary_)
        test_features = test_tf.fit_transform(self.test_documents)
        predicted_labels = clf.predict(test_features)
        # confm = metrics.confusion_matrix(self.test_labels, predicted_labels)
        # print(confm)
        # sns.heatmap(confm.T,square=True,annot=True,fmt='d',cbar=False,cmap=plt.cm.gray_r)
        # plt.xlabel('True label')
        # plt.ylabel('predicted label')
        # plt.show()
        # c_r = metrics.classification_report(self.test_labels, predicted_labels)
        # print(c_r[c_r.index('accuracy')-15:])
        # print(type(c_r))
        return self.assess(predicted_labels)


if __name__ == '__main__':
    nbc = NBC()
    nbc.run()
