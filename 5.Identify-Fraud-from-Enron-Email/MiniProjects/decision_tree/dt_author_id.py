#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

# Needed for this miniproject
from sklearn import tree
from sklearn.metrics import accuracy_score


# Question 1/5: What is the accuracy for 
# decision tree w/ min_samples_split = 40:'
clf = tree.DecisionTreeClassifier(min_samples_split = 40)

print
print
print 'Question #1 / #5:'
print '----------------'
print 'Fitting Data...'
clf.fit(features_train, labels_train)
print 'Fitting Completed.'
print '========'

print 'Making Predictions...'
pred = clf.predict(features_test)
print 'Prediction Completed.'
print '========'

print 'Calculating Accuracy...'
acc_tree = accuracy_score(pred, labels_test)
print 'Acurracy =', acc_tree



# Question 2: How many features are in the dataset
print
print
print 'Question 2:'
print '----------------'
print 'Number of features:', len(features_train[0])

#########################################################


