import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sklearn
import numpy as np 
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("machinelearning/creditcard.csv")
print(df.describe())

#Divide the Dataset between training and test

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
feature_names = df.iloc[:, 1:30].columns
target = df.iloc[:1, 30:].columns
data_features = df[feature_names]
data_target = df[target]
from sklearn.model_selection import train_test_split
np.random.seed(123)
X_train, X_test, y_train, y_test = train_test_split(data_features, data_target,train_size = 0.70, test_size = 0.30, random_state = 1)

# Use XGBoost model

import xgboost as xgb
xg = xgb.XGBClassifier()
xg.fit(X_train, y_train)
predxg = xg.predict(X_test)
matrixxg = confusion_matrix(y_test, predxg)
accuracy_scorexg=accuracy_score(y_test, predxg)
classification_reportxg=classification_report(y_test, predxg,output_dict=True)

#Use LogisticRegression model

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train, y_train)
predlr = lr.predict(X_test)
matrixlr = confusion_matrix(y_test, predlr)
accuracy_scorelr=accuracy_score(y_test, predlr)
classification_reportlr=classification_report(y_test, predlr,output_dict=True)

# Create Experiment MLflow

import mlflow
mlflow.set_tracking_uri("http://172.18.20.48:31560")
experiment_name = "XGBoost and Logistic Regression Experiment"
experiment_id = mlflow.create_experiment(experiment_name) if mlflow.get_experiment_by_name(experiment_name) is None else mlflow.get_experiment_by_name(experiment_name).experiment_id

# Write the model metrics to the MLflow:

# After running the scripts, you can go to http://172.18.20.48:31560 
# to check the two models and compare between them.

mlflow.set_experiment("XGBoost and Logistic Regression Experiment")
mlflow.set_tracking_uri(uri="http://172.18.20.48:31560")
with mlflow.start_run(run_name="xgboost model"):
    #mlflow.log_params(params)
    mlflow.log_metrics({
        'accuracy': classification_reportxg['accuracy'],
        'recall_class_0': classification_reportxg['0']['recall'],
        'recall_class_1': classification_reportxg['1']['recall'],
        'f1_score_macro': classification_reportxg['macro avg']['f1-score']
    })
    mlflow.sklearn.log_model(xg, "xgboost model", registered_model_name="XGBoostModel")

with mlflow.start_run(run_name="LogisticRegression model"):
    #mlflow.log_params(params)
    mlflow.log_metrics({
        'accuracy': classification_reportlr['accuracy'],
        'recall_class_0': classification_reportlr['0']['recall'],
        'recall_class_1': classification_reportlr['1']['recall'],
        'f1_score_macro': classification_reportlr['macro avg']['f1-score']
    })
    mlflow.sklearn.log_model(lr, "LogisticRegression model", registered_model_name="LogisticRegressionModel")

