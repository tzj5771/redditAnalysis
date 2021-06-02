import numpy as np
from sklearn import tree, metrics, model_selection, __all__, svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from Task_3.data_load_handle import DataLoadHandle


class SVM(DataLoadHandle):
    def __init__(self):
        super().__init__()

    def run(self, c=1.0, gamma='scale', is_print=True):
        # 计算矩阵
        tt = TfidfVectorizer(max_df=0.5)
        tf = tt.fit_transform(self.train_documents)
        # 非线性SVM模型
        # ovr:一对多策略，ovo表示一对一
        rbf_svm = SVC(C=c, gamma=gamma, kernel='rbf', decision_function_shape='ovo')
        # 模型在训练数据集上的拟合
        rbf_svm.fit(tf, self.train_labels)
        test_tf = TfidfVectorizer(max_df=0.5, vocabulary=tt.vocabulary_)
        test_features = test_tf.fit_transform(self.test_documents)
        predicted = rbf_svm.predict(test_features)
        return self.assess(predicted, is_print)

    def optimal_attempt(self):
        self.run(is_print=False)
        # epsilon = np.arange(0.1, 1.5, 0.2) 'epsilon': epsilon,
        C = [1, 10, 100, 200]
        gamma = [1, 0.1, 0.01, 0.001, 0.002]
        parameters = {'kernel': ['rbf'], 'C': C, 'gamma': gamma}
        tt = TfidfVectorizer(max_df=0.5)
        tf = tt.fit_transform(self.train_documents)
        grid_svr = model_selection.GridSearchCV(estimator=svm.SVR(max_iter=10000), param_grid=parameters,
                                                return_train_score=True,
                                                scoring='neg_mean_squared_error', cv=5, verbose=1, n_jobs=2)
        nature = []
        for d in self.train_labels:
            if d not in nature:
                nature.append(d)

        target_list = []
        for d in self.train_labels:
            target_list.append(nature.index(str(d)))

        grid_svr.fit(tf, target_list)
        print(grid_svr.best_params_, grid_svr.best_score_)
        test_tf = TfidfVectorizer(max_df=0.5, vocabulary=tt.vocabulary_)
        test_features = test_tf.fit_transform(self.test_documents)
        # pred_grid_svr = grid_svr.predict(test_features)
        test_nature = []
        for d in self.test_labels:
            if d not in test_nature:
                test_nature.append(d)

        test_target_list = []
        for d in self.test_labels:
            test_target_list.append(test_nature.index(str(d)))
        # print(metrics.mean_squared_error(test_target_list, pred_grid_svr))
        # print(metrics.accuracy_score(test_target_list, pred_grid_svr))
        # print('best_estimator_:', grid_svr.best_estimator_)
        # print('best_params_:', grid_svr.best_params_)
        # print('best_params_:', grid_svr.cv_results_['params'][grid_svr.best_index_])
        # print('best_score_:', grid_svr.best_score_)
        # print('scorer_:', grid_svr.scorer_)
        # print('n_splits_:', grid_svr.n_splits_)
        self.run(grid_svr.best_params_["C"], grid_svr.best_params_["gamma"], is_print=False)


if __name__ == '__main__':
    svn = SVM()
    svn.optimal_attempt()
    # 0.03918495297805643
    # 0.08150470219435736
    # print(svn.run())
