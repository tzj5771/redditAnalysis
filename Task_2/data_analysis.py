import cufflinks as cufflinks
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import RANSACRegressor, LinearRegression, TheilSenRegressor
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, median_absolute_error, \
    r2_score
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso, ElasticNet, BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
import cufflinks
cufflinks.go_offline(connected=True)


data = pd.read_csv('../data/analysis_data.csv')
# 查看数据记录的长度，共1030行
print(len(data))
data.columns = ['title', 'comment', "title_length", "comment_length"]
# 查看前五行数据
print(data.head())
data['title_length'].iplot(kind='hist', xTitle='length', yTitle='count', title='Article length distribution')
