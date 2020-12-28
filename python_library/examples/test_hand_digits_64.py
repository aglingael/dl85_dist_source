from sklearn.svm import SVC
from sklearn.datasets import load_iris, load_digits, fetch_openml
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelBinarizer, KBinsDiscretizer, Binarizer
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import check_random_state
from dl85 import DL85Booster, DL85Classifier, BOOST_SVM2
import xgboost as xgb
import time
import numpy as np
import pandas as pd
import sys

depth, time_limit, N_FOLDS = 2, 0, 5

file = open("../output/nist_" + str(depth) + ".txt", "w")

train = np.genfromtxt("../datasets/boosting/nist/optdigits.tra", delimiter=",")
test = np.genfromtxt("../datasets/boosting/nist/optdigits.tes", delimiter=",")
# split features and target
X_train, y_train = train[:, :-1], train[:, -1]
X_test, y_test = test[:, :-1], test[:, -1]
# select a slice of training data
# X_train, _, y_train, _ = train_test_split(X_train, y_train, stratify=y_train, train_size=500)
# convert values to int
X_train, y_train = X_train.astype('int32'), y_train.astype('int32')
X_test, y_test = X_test.astype('int32'), y_test.astype('int32')
# binarize the features
enc = Binarizer(threshold=1)
X_train = enc.fit_transform(X_train)
X_test = enc.fit_transform(X_test)
# create 2 classes even or odd
# biner = lambda x: x % 2
# y_train = biner(y_train)
# y_test = biner(y_test)
# another way to create more complex binarization
# def binner(x):
#    if x in [5, 2]:
#        return 0
#    elif x in [3, 8]:
#        return 1
#    elif x in [1, 7, 4]:
#        return 2
#    elif x in [0, 9, 6]:
#        return 3
def binner(x):
    if x in [0, 1, 2, 3]:
        return 0
    elif x in [4, 5, 6]:
        return 1
    elif x in [7, 8, 9]:
        return 2
y_train = np.array(list(map(binner, y_train)))
y_test = np.array(list(map(binner, y_test)))
print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
print(set(y_train), set(y_test))
file.write(str(X_train.shape) + " " + str(y_train.shape) + "\n")
file.write(str(X_test.shape) + " " + str(y_test.shape) + "\n")
file.write(str(set(y_train)) + " " + str(set(y_test)) + "\n")

print("Optical Recognition of Handwritten Digits Data Set")

from sklearn.metrics import confusion_matrix
# clf = DL85Booster(max_depth=depth, min_sup=1, max_estimators=3, opti_gap=0, step=.1, tolerance=0.00001, model=BOOST_SVM2, time_limit=time_limit, quiet=True)
# clf = DL85Booster(max_depth=depth, min_sup=1, max_estimators=2, opti_gap=0, step=.001, tolerance=0.0000001, model=BOOST_SVM2, time_limit=time_limit, quiet=True)
clf = DL85Booster(max_depth=depth, min_sup=1, regulator=0.2009931035749624, opti_gap=0, step=.006, tolerance=0.000001, model=BOOST_SVM2, time_limit=time_limit, quiet=True)
# clf = DL85Booster(max_depth=depth, min_sup=1, regulator=0.2, time_limit=time_limit)
# 0.05099310357496239 4
# 0.2009931035749624 3
# 0.07771185357496238 5
start = time.perf_counter()
print("Model building...")
clf.fit(X_train, y_train)
duration = time.perf_counter() - start
print("Model built. Duration of building =", round(duration, 4))
y_pred = clf.predict(X_test)
print("Confusion Matrix below")
print(confusion_matrix(y_test, y_pred))
print("Accuracy DL8.5 on training set =", round(clf.accuracy_, 4))
print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4))
print(clf.problem)
print(clf.regulator, clf.n_estimators_)
for c in clf.estimators_:
    print(c.tree_)

max_trees = clf.n_estimators_


print()
clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=depth), n_estimators=max_trees)
# clf = DecisionTreeClassifier(max_depth=depth)
# clf = DL85Booster(max_depth=depth, min_sup=1, regulator=0.007137981694607998, time_limit=time_limit)
start = time.perf_counter()
print("Model building...")
clf.fit(X_train, y_train)
duration = time.perf_counter() - start
print("Model built. Duration of building =", round(duration, 4))
y_pred = clf.predict(X_test)
print("Confusion Matrix below")
print(confusion_matrix(y_test, y_pred))
print("Accuracy DL8.5 on training set =", round(accuracy_score(y_train, clf.predict(X_train)), 4))
print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4), "\n\n\n")


print()
clf = AdaBoostClassifier(base_estimator=DL85Classifier(max_depth=depth), n_estimators=max_trees)
# clf = DL85Booster(max_depth=depth, min_sup=1, regulator=0.007137981694607998, time_limit=time_limit)
start = time.perf_counter()
print("Model building...")
clf.fit(X_train, y_train)
duration = time.perf_counter() - start
print("Model built. Duration of building =", round(duration, 4))
y_pred = clf.predict(X_test)
print("Confusion Matrix below")
print(confusion_matrix(y_test, y_pred))
print("Accuracy DL8.5 on training set =", round(accuracy_score(y_train, clf.predict(X_train)), 4))
print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4), "\n\n\n")



print()
clf = AdaBoostClassifier(base_estimator=DL85Classifier(max_depth=depth), n_estimators=max_trees, algorithm="SAMME")
# clf = DL85Booster(max_depth=depth, min_sup=1, regulator=0.007137981694607998, time_limit=time_limit)
start = time.perf_counter()
print("Model building...")
clf.fit(X_train, y_train)
duration = time.perf_counter() - start
print("Model built. Duration of building =", round(duration, 4))
y_pred = clf.predict(X_test)
print("Confusion Matrix below")
print(confusion_matrix(y_test, y_pred))
print("Accuracy DL8.5 on training set =", round(accuracy_score(y_train, clf.predict(X_train)), 4))
print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4), "\n\n\n")



print()
clf = GradientBoostingClassifier(max_depth=depth, n_estimators=max_trees)
# clf = DL85Booster(max_depth=depth, min_sup=1, regulator=0.007137981694607998, time_limit=time_limit)
start = time.perf_counter()
print("Model building...")
clf.fit(X_train, y_train)
duration = time.perf_counter() - start
print("Model built. Duration of building =", round(duration, 4))
y_pred = clf.predict(X_test)
print("Confusion Matrix below")
print(confusion_matrix(y_test, y_pred))
print("Accuracy DL8.5 on training set =", round(accuracy_score(y_train, clf.predict(X_train)), 4))
print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4), "\n\n\n")
sys.exit(0)


for d in range(1, depth+1):
    print()
    print("dl85 depth =", d)
    file.write("\ndl85 depth=" + str(d) + "\n")
    clf = DL85Classifier(max_depth=d, min_sup=1, time_limit=time_limit)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("train_acc:", accuracy_score(y_train, clf.predict(X_train)), "test_acc:", accuracy_score(y_test, y_pred))
    file.write("train_acc: " + str(accuracy_score(y_train, clf.predict(X_train))) + "\n")
    file.write("test_acc: " + str(accuracy_score(y_test, y_pred)) + "\n")
    file.flush()

    print()
    print("cart depth =", d)
    file.write("\ncart depth=" + str(d) + "\n")
    clf = DecisionTreeClassifier(max_depth=d, min_samples_leaf=1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("train_acc:", accuracy_score(y_train, clf.predict(X_train)), "test_acc:", accuracy_score(y_test, y_pred))
    file.write("train_acc: " + str(accuracy_score(y_train, clf.predict(X_train))) + "\n")
    file.write("test_acc: " + str(accuracy_score(y_test, y_pred)) + "\n")
    file.flush()


# print()
# print("dl85 depth=2")
# clf = DL85Classifier(max_depth=depth, min_sup=1, time_limit=time_limit)
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print("train_acc:", accuracy_score(y_train, clf.predict(X_train)), "test_acc:", accuracy_score(y_test, y_pred))
#
#
# print()
# print("cart depth=2")
# clf = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=1)
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print("train_acc:", accuracy_score(y_train, clf.predict(X_train)), "test_acc:", accuracy_score(y_test, y_pred))
# # sys.exit(0)


print()
print("lpdl8 d" + str(depth))
file.write("\n\nlpdl85 depth=" + str(depth) + "\n")
parameters = {'regulator': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 10, 100, 1000, 10000, 100000, 1000000]}
grid = GridSearchCV(estimator=DL85Booster(max_depth=depth, min_sup=1, time_limit=time_limit, max_estimators=0, model=BOOST_SVM2),
                    param_grid=parameters, scoring='accuracy', cv=4, n_jobs=-1, verbose=10)
grid.fit(X_train, y_train)
max_trees = grid.best_estimator_.n_estimators_
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("max_trees:", max_trees)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", max_trees, "regulator", grid.best_params_['regulator'])
file.write("best params: " + str(grid.best_params_) + "\n")
file.write('n_trees: ' + str(max_trees) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("AdaBoost non-linear max_trees")
file.write("\n\nAdaBoost non-linear max_trees\n")
clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=depth), n_estimators=max_trees)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, clf.predict(X_train)), accuracy_score(y_test, y_pred)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", len(clf.estimators_))
file.write('n_trees: ' + str(len(clf.estimators_)) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("AdaBoost non-linear")
file.write("\n\nAdaBoost non-linear\n")
param_grid_ada = {'n_estimators': [50, 100, 1000]}
grid = GridSearchCV(estimator=AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=depth)), param_grid=param_grid_ada, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", len(grid.best_estimator_.estimators_))
file.write("best params: " + str(grid.best_params_) + "\n")
file.write('n_trees: ' + str(len(grid.best_estimator_.estimators_)) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("XGBoost non-linear maxtrees")
file.write("\n\nXGBoost non-linear maxtrees\n")
param_grid_xgb = {'objective': ['binary:logistic', 'binary:logitraw']}
grid = GridSearchCV(estimator=xgb.XGBClassifier(n_estimators=max_trees, max_depth=depth), param_grid=param_grid_xgb, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", grid.best_estimator_.n_estimators, "objective", grid.best_params_['objective'])
file.write("best params: " + str(grid.best_params_) + "\n")
file.write('n_trees: ' + str(grid.best_estimator_.n_estimators) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("XGBoost non-linear")
file.write("\n\nXGBoost non-linear\n")
param_grid_xgb = {'n_estimators': [50, 100, 1000], 'objective': ['binary:logistic', 'binary:logitraw']}
grid = GridSearchCV(estimator=xgb.XGBClassifier(max_depth=depth), param_grid=param_grid_xgb, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", grid.best_estimator_.n_estimators, "objective", grid.best_params_['objective'])
file.write("best params: " + str(grid.best_params_) + "\n")
file.write('n_trees: ' + str(grid.best_estimator_.n_estimators) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("RF non-linear maxtrees")
file.write("\n\nRF non-linear maxtrees\n")
clf = RandomForestClassifier(max_depth=depth, n_estimators=max_trees)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, clf.predict(X_train)), accuracy_score(y_test, y_pred)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", len(clf.estimators_))
file.write('n_trees: ' + str(len(clf.estimators_)) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("RF non-linear")
file.write("\n\nRF non-linear\n")
param_grid_rf = {'n_estimators': [50, 100, 1000]}
grid = GridSearchCV(estimator=RandomForestClassifier(max_depth=depth), param_grid=param_grid_rf, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", len(grid.best_estimator_.estimators_))
file.write("best params: " + str(grid.best_params_) + "\n")
file.write('n_trees: ' + str(len(grid.best_estimator_.estimators_)) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("GB non-linear maxtrees")
file.write("\n\nGB non-linear maxtrees\n")
clf = GradientBoostingClassifier(max_depth=depth, n_estimators=max_trees)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, clf.predict(X_train)), accuracy_score(y_test, y_pred)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", clf.n_estimators)
file.write('n_trees: ' + str(clf.n_estimators) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("GB non-linear")
file.write("\n\nGB non-linear\n")
param_grid_gb = {'n_estimators': [50, 100, 1000]}
grid = GridSearchCV(estimator=GradientBoostingClassifier(max_depth=depth), param_grid=param_grid_gb, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_acc:", train_acc, "test_acc:", test_acc, "n_trees", grid.best_estimator_.n_estimators)
file.write("best params: " + str(grid.best_params_) + "\n")
file.write('n_trees: ' + str(grid.best_estimator_.n_estimators) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("SVM linear")
file.write("\n\nSVM linear\n")
param_grid_linear = {'C': [0.1, 1, 10, 100, 1000], 'kernel': ['linear']}
grid = GridSearchCV(SVC(max_iter=1000), param_grid_linear, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_fold:", train_acc, "test_fold:", test_acc)
file.write("best params: " + str(grid.best_params_) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()
time.sleep(5)


print("\n")
print("SVM non-linear")
file.write("\n\nSVM non-linear\n")
param_grid_poly = {'C': [0.1, 1, 10, 100, 1000], 'kernel': ['poly', 'rbf'], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 'degree': [2, 3, 4]}
grid = GridSearchCV(SVC(max_iter=1000), param_grid_poly, refit=True, verbose=10, cv=4, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
train_acc, test_acc = accuracy_score(y_train, grid.predict(X_train)), accuracy_score(y_test, y_pred)
print(grid.best_params_)
print("train_fold:", train_acc, "test_fold:", test_acc)
file.write("best params: " + str(grid.best_params_) + "\n")
file.write("train_acc: " + str(train_acc) + "\n")
file.write("test_acc: " + str(test_acc) + "\n")
file.flush()