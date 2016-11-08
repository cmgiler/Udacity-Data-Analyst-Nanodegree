#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from time import time

# Import classifiers to test
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

# Import metrics to analyze results
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

# Import functions for cross validation and parameter optimization
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = ['poi', 'salary', 'to_messages', 'deferral_payments', 'total_payments',
       'exercised_stock_options', 'bonus', 'restricted_stock',
       'shared_receipt_with_poi', 'restricted_stock_deferred',
       'total_stock_value', 'expenses', 'loan_advances', 'from_messages',
       'other', 'from_this_person_to_poi', 'poi', 'director_fees',
       'deferred_income', 'long_term_incentive',
       'from_poi_to_this_person'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# List all features
# Count dataset features
# 	Total number of data points
# 	Allocation across classes (POI vs non-POI)
#	Number of features
# 	Number of missing values

print 
print 'DATA POINTS'
print '==========='
print len(data_dict), 'total data points'
count_poi = 0
for person in data_dict:
	if data_dict[person]['poi'] == 1:
		count_poi += 1
print count_poi, 'POI;	', len(data_dict) - count_poi, 'non-POI'


print
print
print 'FEATURES'
print '========'
first_key = data_dict.keys()[0]
print len(data_dict[first_key].keys()), 'features total'
print
print 'Feature breakdown:'
data_types = defaultdict(list)
for key in data_dict[first_key].keys():
	data_type = type(data_dict[first_key][key])
	data_types[data_type].append(key)
print
print 'Data Types:'
for key in data_types:
	print key,':'
#	for item in data_types[key]:
#		print '   ', item
	print data_types[key]
	print '------------'

## Find missing data ('NaN')
print 
print 'MISSING DATA (NaN)'
print '=================='
print 'Count of NaN Values (for each feature) :'
print
# Initialize Counts:
count_nan = defaultdict(int)
for key in data_dict[first_key].keys():
	count_nan[key] = 0
# Increment Counter
for person in data_dict:
	for key in data_dict[person].keys():
		if data_dict[person][key] == 'NaN':
			count_nan[key] += 1
# Sort dictionary by value and print values
for key in sorted(count_nan, key=count_nan.get, reverse=True):
  print key, count_nan[key]

# Count NaN by Data Point:
print 
print
print 'NaN by Data Point'
print '================='
count_nan_ind = defaultdict(int)
for person in data_dict:
	cnt = 0
	for key in data_dict[person].keys():
		if data_dict[person][key] == 'NaN':
			cnt += 1
	count_nan_ind[person] = cnt

for key in sorted(count_nan_ind, key = count_nan_ind.get, reverse=True)[0:14]:
	print key, count_nan_ind[key]

print
print 'LOCKHART EUGENE E:'
print '=================='
print data_dict['LOCKHART EUGENE E']

print 'WHALEY DAVID A:'
print '=================='
print data_dict['WHALEY DAVID A']

### Task 2: Remove outliers
#print data_dict.keys()
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
data_dict.pop('LOCKHART EUGENE E')
#print data_dict.keys()

# Replace NaN values
from sklearn.preprocessing import Imputer
imp = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imp.fit(data_dict)
data_dict = imp.transform(data_dict)


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

'''
for point in data:
	salary = point[0]
	bonus = point[1]
	plt.scatter(salary, bonus)
plt.xlabel('salary')
plt.ylabel('bonus')
plt.show()
'''

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)