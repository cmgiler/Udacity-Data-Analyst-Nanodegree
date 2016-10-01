#!/usr/bin/python

import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture

features_train, labels_train, features_test, labels_test = makeTerrainData()


### the training data (features_train, labels_train) have both "fast" and "slow"
### points mixed together--separate them so we can give them different colors
### in the scatterplot and identify them visually
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==1]


#### initial visualization
'''plt.xlim(0.0, 1.0)
plt.ylim(0.0, 1.0)
plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
plt.legend()
plt.xlabel("bumpiness")
plt.ylabel("grade")
plt.show()'''
################################################################################


### your code here!  name your classifier object clf if you want the 
### visualization code (prettyPicture) to show you the decision boundary

########################################################################
## First, try optimizing a few algorithms on a smaller dataset
'''
features_train = features_train[:len(features_train)/100]
labels_train = labels_train[:len(labels_train)/100]
'''

from sklearn.metrics import accuracy_score

# Create output file
def print_info(iter_ct, algorithm, param1_name, param1_val,	param2_name, param2_val, accuracy, time):
	print '=========', iter_ct, '=========='
	print 'Algorithm :', algorithm
	print param1_name, '=', param1_val
	print param2_name, '=', param2_val
	print 'Accuracy =', accuracy
	print 'Time to complete =', time, 's'
	print

	
def clf_accuracy(clf, features_train, labels_train, features_test, labels_test):
	clf.fit(features_train, labels_train)
	pred = clf.predict(features_test)
	return accuracy_score(pred, labels_test)
	

# Set optimization test sets
c_vals = [10,100,1000,10000]
kernel_vals = ['rbf','linear','poly','sigmoid']
min_samples_split_vals = [1,2,5,10]
splitter_vals = ['best','random']
n_neighbors_vals = [2,3,5,10]
leaf_size_vals = [10,20,30,50]
n_estimators_vals = [10,100,500]

# Run tests
# Import algorithms to use
from sklearn.naive_bayes import GaussianNB
from sklearn import svm, tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from time import time

'''
# Naive Bayes
clf = GaussianNB()
t0 = time()
accuracy = clf_accuracy(clf, features_train, labels_train, features_test, labels_test)
print_info(1, 'Naive-Bayes', '-', '-', '-', '-', accuracy, round(time()-t0, 3))
'''

'''
# SVM
max_acc = 0
max_iter = 0
curr_iter = 1
for param1 in c_vals:
	for param2 in kernel_vals:
		clf = svm.SVC(C = param1, kernel = param2)
		t0 = time()
		accuracy = clf_accuracy(clf, features_train, labels_train,
					features_test, labels_test)
		print_info(curr_iter, 'SVM', 'c', param1, 'kernel', param2,
					accuracy, round(time()-t0, 3))
		if accuracy > max_acc:
			max_acc = accuracy
			max_iter = curr_iter
		curr_iter += 1
print
print 'Max SVM Accuracy:', max_acc, 'at iteration', max_iter
'''

'''
# Decision Tree
max_acc = 0
max_iter = 0
curr_iter = 1
for param1 in min_samples_split_vals:
	for param2 in splitter_vals:
		clf = tree.DecisionTreeClassifier(min_samples_split=param1,
											splitter=param2)
		t0 = time()
		accuracy = clf_accuracy(clf, features_train, labels_train,
					features_test, labels_test)
		print_info(curr_iter, 'Decision Tree', 'min_samples_split', param1, 'splitter', param2,
					accuracy, round(time()-t0, 3))
		if accuracy > max_acc:
			max_acc = accuracy
			max_iter = curr_iter
		curr_iter += 1
print
print 'Max Decision Tree Accuracy:', max_acc, 'at iteration', max_iter
'''	
'''
# K nearest neighbors
max_acc = 0
max_iter = 0
curr_iter = 1
for param1 in n_neighbors_vals:
	for param2 in leaf_size_vals:
		clf = KNeighborsClassifier(n_neighbors = param1, leaf_size = param2)
		t0 = time()
		accuracy = clf_accuracy(clf, features_train, labels_train,
					features_test, labels_test)
		print_info(curr_iter, 'K Nearest Neighbors', 'n_neighbors', param1, 'leaf_size', param2,
					accuracy, round(time()-t0, 3))
		if accuracy > max_acc:
			max_acc = accuracy
			max_iter = curr_iter
			clf_save = clf
		curr_iter += 1
print
print 'Max KNN Accuracy:', max_acc, 'at iteration', max_iter
'''
'''
# AdaBoost
max_acc = 0
max_iter = 0
curr_iter = 1
for param1 in min_samples_split_vals:
	for param2 in n_estimators_vals:
		clf = AdaBoostClassifier(tree.DecisionTreeClassifier(min_samples_split = param1),
							n_estimators = param2)
		t0 = time()
		accuracy = clf_accuracy(clf, features_train, labels_train,
					features_test, labels_test)
		print_info(curr_iter, 'AdaBoost', 'min_samples_split', param1, 'n_estimators', param2,
					accuracy, round(time()-t0, 3))
		if accuracy > max_acc:
			max_acc = accuracy
			max_iter = curr_iter
			clf_save = clf
		curr_iter += 1
print
print 'Max AdaBoost Accuracy:', max_acc, 'at iteration', max_iter
'''
'''
# Random Forest
max_acc = 0
max_iter = 0
curr_iter = 1
for param1 in n_estimators_vals:
	for param2 in min_samples_split_vals:
		clf = RandomForestClassifier(n_estimators=param1, min_samples_split=param2)
		t0 = time()
		accuracy = clf_accuracy(clf, features_train, labels_train,
					features_test, labels_test)
		print_info(curr_iter, 'Random Forest', 'n_estimators', param1, 'min_samples_split', param2,
					accuracy, round(time()-t0, 3))
		if accuracy > max_acc:
			max_acc = accuracy
			max_iter = curr_iter
			clf_save = clf
		curr_iter += 1
print
print 'Max Random Forest Accuracy:', max_acc, 'at iteration', max_iter
'''

clf = KNeighborsClassifier(n_neighbors=3, leaf_size=10)
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
accuracy = accuracy_score(pred, labels_test)
print_info('=','KNN','n_neighbors',3,'leaf_size',10,accuracy,'-')

try:
	prettyPicture(clf, features_test, labels_test)
except NameError:
    pass
