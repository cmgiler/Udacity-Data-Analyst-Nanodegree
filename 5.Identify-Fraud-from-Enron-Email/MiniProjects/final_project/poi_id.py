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
import re

# Import classifiers to test
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
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

# Import user functions
from my_functions import *


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = ['poi', 'salary', 'to_messages', 'deferral_payments', 'total_payments',
       'exercised_stock_options', 'bonus', 'restricted_stock',
       'shared_receipt_with_poi', 'restricted_stock_deferred',
       'total_stock_value', 'expenses', 'loan_advances', 'from_messages',
       'other', 'from_this_person_to_poi', 'director_fees',
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


total_data_points, count_poi = num_datapoints(data_dict)
print 
print 'DATA POINTS'
print '==========='
print total_data_points, 'data points total'
print count_poi, 'POI;	', total_data_points - count_poi, 'non-POI'

feature_count, feature_data_types = num_features(data_dict)
print
print
print 'FEATURES'
print '========'
print feature_count, 'features total'
print
print 'Data Types:'
for key in feature_data_types:
	print key,':'
#	for item in data_types[key]:
#		print '   ', item
	print feature_data_types[key]
	print '------------'

## Find missing data ('NaN')
count_nan, count_nan_ind = num_nan_values(data_dict)
print 
print 'MISSING DATA (NaN)'
print '=================='
print 'Count of NaN Values (for each feature) :'
print
for key in sorted(count_nan, key=count_nan.get, reverse=True):
  print key, count_nan[key]
print 
print
print 'NaN by Data Point'
print '================='
for key in sorted(count_nan_ind, key = count_nan_ind.get, reverse=True)[0:14]:
	print key, count_nan_ind[key]



### Task 2: Remove outliers
#print data_dict.keys()
outliers = ['TOTAL','THE TRAVEL AGENCY IN THE PARK','LOCKHART EUGENE E']
data_dict = remove_outliers(data_dict, outliers)
#print data_dict.keys()


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
data_dict = preprocess_data(data_dict)
data_dict, features_list = add_features(data_dict, features_list)

total_data_points_new, count_poi_new = num_datapoints(data_dict)
print '=================='
print 'Total Data Points:', total_data_points, '->', total_data_points_new
print 'POI Count:', count_poi, '->', count_poi_new

count_nan_new, count_nan_ind_new = num_nan_values(data_dict)
nan_cnt_old = 0
nan_cnt_new = 0
for key in sorted(count_nan, key=count_nan.get, reverse=True):
  nan_cnt_old += count_nan[key]
  nan_cnt_new += count_nan_new[key]
print 'Total NaN Values:', nan_cnt_old, '->', nan_cnt_new

my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Select Features
top_features, score_pairs = select_features(data_dict, 
                                            features_list, 
                                            select_count=10,
                                            plot_results=False)
print top_features

ranking_pairs = rank_features(data_dict, 
                              top_features, 
                              plot_results=False)

# Provided to give you a starting point. Try a variety of classifiers.
top_features = ['poi',
                'total_stock_value',
                'exercised_stock_options',
                'deferred_income',
                'bonus',
                'salary']
# Reload data using only top 10 features found through K-Best Selection
data = featureFormat(data_dict, top_features, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Feature scaling
from sklearn import preprocessing
features = preprocessing.MinMaxScaler().fit_transform(features)

from sklearn.cross_validation import StratifiedShuffleSplit
cv = StratifiedShuffleSplit(labels)

models = [GaussianNB(), LinearSVC(), LogisticRegression(), 
          DecisionTreeClassifier(), KNeighborsClassifier(), AdaBoostClassifier(),
          RandomForestClassifier()]

test_results = {}
for i in range(len(models)):
    clf = models[i]
    clf_str = re.split(r'\(', str(clf))[0]
    test_results[clf_str] = {}
    test_results[clf_str]['Accuracy'] = test_algorithm(clf,features,labels,'accuracy',cv)
    test_results[clf_str]['Precision'] = test_algorithm(clf,features,labels,'precision',cv)
    test_results[clf_str]['Recall'] = test_algorithm(clf,features,labels,'recall',cv)

df_results = pd.DataFrame.from_dict(test_results).T

#plot_df_results(df_results)

'''
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
'''
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
features_list = top_features
clf = GaussianNB()
dump_classifier_and_data(clf, my_dataset, features_list)

import tester
tester.main()
