# -*- coding: utf-8 -*-
"""Linear_Regression

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xb1hGmtmwoH0Obi3BlyPPdczIR2pQJiy
"""
# WRITEN BY RATTIKAN NUALSRI, 27-06-2024, version 1.0

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from google.colab import drive
drive.mount('/content/gdrive')


warnings.filterwarnings("ignore")

np.random.seed(12345)

data = pd.read_csv("/content/gdrive/MyDrive/Colab Notebooks/Supervised_Learning/DataSet/Salary_DataSet/salary_dataset.csv")
data

# 2 Clean data
# Handle missing values and outliers data
data.info()

data.dropna(axis=0, inplace=True)

data.describe()

data = data[data["gpa"] <= 4]

data.describe()

# 3 Split data for train and test set
target_name = "salary"
feature_name = list(data.columns.drop(target_name))

x = data[feature_name]
y = data[target_name]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, shuffle=True)

# 4 Data preparation
numerical_feature = ["age", "experience", "gpa"]
categorical_feature = ["degree", "position"]

for feature in categorical_feature:
    print(feature, " : ", np.unique(x_train[feature]))

ordinal_feature = ["degree"]
nominal_feature = ["position"]

np.unique(data["degree"])

# ordinal_encoder = OrdinalEncoder(categories=[["bachelor", "doctorate", "master"]], dtype = int)
# x_train[ordinal_feature] = ordinal_encoder.fit(x_train[ordinal_feature])

# 4.1 Ordinal Encoding
# Training Set
categories = [np.array(["bachelor", "doctorate", "master"], dtype=object), ]
data["degree"]
data_Degree = pd.DataFrame(data["degree"])

data_Degree
# oe = OrdinalEncoder(dtype=int)
# x_train = oe.fit(categories)

data_Degree.value_counts()
data_Degree

oe = OrdinalEncoder(dtype = object)
oe.fit(data_Degree)
# data_Degree_Ordinal_Encoder = oe.transform(data_Degree)

# oe.transform(x_train[ordinal_feature])

# encoding_View = data_Degree.assign(encode = data_Degree_Ordinal_Encoder)

# # encoding_View

# Train Set
ordinal_encoder_train = OrdinalEncoder(dtype = object)
ordinal_encoder_train.fit(x_train[ordinal_feature])
x_train[ordinal_feature] = ordinal_encoder_train.transform(x_train[ordinal_feature])

# Test Set
ordinal_encoder_test = OrdinalEncoder(dtype = object)
ordinal_encoder_test.fit(x_test[ordinal_feature])
x_test[ordinal_feature] = ordinal_encoder_test.transform(x_test[ordinal_feature])
# x_train[ordinal_feature]


# x_1_train = OrdinalEncoder(dtype  = object)
# x_1_train.fit(categories)
# x_1_train
# x_train[ordinal_feature] = ordinal_encoder.fit_transform(x_train[ordinal_feature])
x_test[ordinal_feature]

# 4.2 One Hot Encoding
one_hot_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
one_hot_encoder.fit(x_train[nominal_feature])

one_hot_feature = []
for i, feature in enumerate(nominal_feature):
    for cate in one_hot_encoder.categories_[i]:
        one_hot_feature_name = str(feature) + "_" + str(cate)
        one_hot_feature.append(one_hot_feature_name)
nominal_feature

# Train Set
x_train[one_hot_feature] = one_hot_encoder.transform(x_train[nominal_feature])
x_train.drop(nominal_feature, axis=1, inplace=True)

# Test Set
x_test[one_hot_feature] = one_hot_encoder.transform(x_test[nominal_feature])
x_test.drop(nominal_feature, axis=1, inplace=True)

# 5 Model Creation
reg = LinearRegression()

# Train Model
reg.fit(x_train, y_train)

# Model's Weight and Bias
reg.coef_

reg.intercept_

# 6 Prediction
y_pred_train = reg.predict(x_train)

y_pred_test = reg.predict(x_test)

# 7 Model Evaluate
# Train Set Scoring
print("r2_Score: \t\t\t", r2_score(y_train, y_pred_train))
print("Mean Squared Error: \t\t", mean_squared_error(y_train, y_pred_train))
print("Mean Absolute Error: \t\t", mean_absolute_error(y_train, y_pred_train))
print("Mean Absolute Percentage Error: ", mean_absolute_percentage_error(y_train, y_pred_train))

plt.scatter(y_pred_train, y_train)
plt.plot(y_pred_train, y_pred_train, color = "red")
plt.title("Scatter Plot between Predict and Actual Values")
plt.xlabel("Predict")
plt.ylabel("Actual")

# Test Set Scoring
print("r2_Score: \t\t\t", r2_score(y_test, y_pred_test))
print("Mean Squared Error: \t\t", mean_squared_error(y_test, y_pred_test))
print("Mean Absolute Error: \t\t", mean_absolute_error(y_test, y_pred_test))
print("Mean Absolute Percentage Error: ", mean_absolute_percentage_error(y_test, y_pred_test))

plt.scatter(y_pred_test, y_test)
plt.plot(y_pred_test, y_pred_test, color = "red")
plt.title("Scatter Plot between Predict and Actual Values")
plt.xlabel("Predict")
plt.ylabel("Actual")

