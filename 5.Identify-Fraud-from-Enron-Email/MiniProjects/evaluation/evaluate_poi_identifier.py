#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 
print
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = \
	train_test_split(features, labels, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
print 'Accuracy:', accuracy_score(pred, labels_test)
print
print 'Number of POIs:', sum(labels_test)
print 'Total people in test set:', len(labels_test)
print
print 'Test Set', 'Prediction', 'Diff'
for i in range(len(labels_test)):
	print labels_test[i], pred[i], labels_test[i]-pred[i]
print
from sklearn.metrics import precision_score, recall_score
print 'Precision score:', precision_score(labels_test, pred)
print 'Recall score:', recall_score(labels_test, pred)
