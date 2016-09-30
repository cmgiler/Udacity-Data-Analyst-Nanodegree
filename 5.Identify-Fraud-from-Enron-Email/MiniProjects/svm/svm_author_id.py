#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
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
# Create SVM and predict on test features
from sklearn.svm import SVC


''' Optimizing C:
# Use data subset:
features_train = features_train[:len(features_train)/100] 
labels_train = labels_train[:len(labels_train)/100] 

for i in [10, 100, 1000, 10000]:
	print '============'
	print 'i =', i, ':'
	print '============'
	#print 'calculating clf...'
	clf = SVC(kernel='rbf', C=i)
	#print 'Done'

	#print 'fitting data...'
	t0 = time()
	clf.fit(features_train, labels_train)
	#print 'Done'
	print "training time:", round(time()-t0,3),"s"

	t0 = time()
	#print 'making prediction...'
	pred = clf.predict(features_test)
	#print 'Done'
	print "predicting time:", round(time()-t0,3),"s"

	# Check accuracy of predictions
	from sklearn.metrics import accuracy_score

	#print 'calculating prediction accuracy...'
	pred_accuracy = accuracy_score(labels_test, pred)
	#print 'Done'

	print 'Accuracy:', pred_accuracy
	'''



print 'calculating clf...'
clf = SVC(kernel='rbf', C=10000)
print 'Done'
print '========'
print 'fitting data...'
t0 = time()
clf.fit(features_train, labels_train)
print 'Done'
print "training time:", round(time()-t0,3),"s"
print '========'
t0 = time()
print 'making prediction...'
pred = clf.predict(features_test)
print 'Done'
print "predicting time:", round(time()-t0,3),"s"
print '========'

# Check accuracy of predictions
from sklearn.metrics import accuracy_score

print 'calculating prediction accuracy...'
pred_accuracy = accuracy_score(labels_test, pred)
print 'Done'
print '========'
print 'Accuracy:', pred_accuracy

## Calculating predictions for element 10, 26, 50
#for i in [10, 26, 50]:
#	print 'Prediction for element', i, ':', pred[i]

count = 0;
test_class = 1;
for elem in pred:
	if elem == test_class:
		count += 1

print count, 'predictions for class', test_class


#########################################################


