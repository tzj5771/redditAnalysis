from sklearn import tree, metrics
from sklearn.feature_extraction.text import TfidfVectorizer

from Task_3.data_load_handle import DataLoadHandle


class DT(DataLoadHandle):
    def __init__(self):
        super().__init__()

    def run(self):
        # 计算矩阵
        tt = TfidfVectorizer(max_df=0.5)
        tf = tt.fit_transform(self.train_documents)
        clf = tree.DecisionTreeClassifier(criterion="entropy", splitter="random", min_samples_split=4)  # 实例化
        clf = clf.fit(tf, self.train_labels)  # 用训练集数据训练模型
        # 模型预测
        test_tf = TfidfVectorizer(max_df=0.5, vocabulary=tt.vocabulary_)
        test_features = test_tf.fit_transform(self.test_documents)
        predicted = clf.predict(test_features)
        return self.assess(predicted)


if __name__ == '__main__':
    dt = DT()
    print(dt.run())
