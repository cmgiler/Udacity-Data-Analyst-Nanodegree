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

# Import metrics to analyze results
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

# Import functions for cross validation and parameter optimization
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split

# Import user-defined functions
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
       'from_poi_to_this_person']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### List total number of data points, and data point split between POI and non-POI
total_data_points, count_poi = num_datapoints(data_dict)
print 
print 'DATA POINTS'
print '==========='
print total_data_points, 'data points total'
print count_poi, 'POI;	', total_data_points - count_poi, 'non-POI'

### List total number of features
feature_count, feature_data_types = num_features(data_dict)
print
print
print 'FEATURES'
print '========'
print feature_count, 'features total'
print

### Print feature data types, grouped by type
print 'Data Types:'
for key in feature_data_types:
	print key,':'
	print feature_data_types[key]
	print '------------'

### List number of missing data points ('NaN') for each feature
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

### List number of missing features for each data point, in descending order
print 'NaN by Data Point'
print '================='
for key in sorted(count_nan_ind, key = count_nan_ind.get, reverse=True)[0:14]:
	print key, count_nan_ind[key]
print
print



### Task 2: Remove outliers
outliers = ['TOTAL','THE TRAVEL AGENCY IN THE PARK','LOCKHART EUGENE E']
data_dict = remove_outliers(data_dict, outliers)



### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

### Replace NaN values with median values for feature over all data points
data_dict = preprocess_data(data_dict)

### Add new features to data dictionary
###   - fraction_from_poi = from_poi_to_this_person / from_messages
###   - fraction_to_poi = from_this_person_to_poi / to_messages
data_dict, features_list = add_features(data_dict, features_list)

### Print new count of data points and POI data points
total_data_points_new, count_poi_new = num_datapoints(data_dict)
print '=================='
print 'Total Data Points:', total_data_points, '->', total_data_points_new
print 'POI Count:', count_poi, '->', count_poi_new

### Print new total number of NaN values in data dictionary
count_nan_new, count_nan_ind_new = num_nan_values(data_dict)
nan_cnt_old = 0
nan_cnt_new = 0
for key in sorted(count_nan, key=count_nan.get, reverse=True):
  nan_cnt_old += count_nan[key]
  nan_cnt_new += count_nan_new[key]
print 'Total NaN Values:', nan_cnt_old, '->', nan_cnt_new

### Save updated 'data_dict' to variable named 'my_dataset' to dump at end of script
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
                                            select_count=8,
                                            plot_results=False)
print
print 'Top Features'
print '============'
print top_features
print

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

# Reload data using only top 5 features found through K-Best Selection and Feature Ranking
data = featureFormat(data_dict, top_features, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Feature scaling
from sklearn import preprocessing
features = preprocessing.MinMaxScaler().fit_transform(features)

### Test a number of different models with their default parameters to determine
### which to explore further
### Test using cross-validation w/ a Stratified Shuffle Split 
### (average score over 100 pseudo-randomized iterations)
models = [GaussianNB(), LinearSVC(), LogisticRegression(), 
          DecisionTreeClassifier(), KNeighborsClassifier(), AdaBoostClassifier(),
          RandomForestClassifier()]

from sklearn.cross_validation import StratifiedShuffleSplit
cv = StratifiedShuffleSplit(labels, n_iter = 50, test_size = 0.1, random_state = 10)

test_results = {}
for i in range(len(models)):
    clf = models[i]
    clf_str = re.split(r'\(', str(clf))[0]
    test_results[clf_str] = {}
    test_results[clf_str]['Accuracy'] = test_algorithm(clf,features,labels,'accuracy',cv)
    test_results[clf_str]['Precision'] = test_algorithm(clf,features,labels,'precision',cv)
    test_results[clf_str]['Recall'] = test_algorithm(clf,features,labels,'recall',cv)

df_results = pd.DataFrame.from_dict(test_results).T
plot_df_results(df_results)

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

### Find best parameters for AdaBoostClassifier and RandomForestClassifier
'''
print
print 'Optimized Parameters'
print '===================='
rfc = RandomForestClassifier()
parameters_rfc = {'n_estimators':[1, 2, 5, 10, 20, 40, 100], 
                  'min_samples_split':[2, 3, 4, 5, 6, 7, 8], 
                  'min_samples_leaf':[1, 2, 3, 5, 10, 15]}
rfc_optim = GridSearchCV(rfc, parameters_rfc)
rfc_optim.fit(features, labels)
print 'RandomForestClassifier():'
print rfc_optim.best_params_

abc = AdaBoostClassifier()
parameters_abc = {'n_estimators':[2, 5, 10, 15, 20, 30, 40, 50], 
                  'algorithm':('SAMME.R','SAMME'), 
                  'random_state':[10, 20, 30, 40, 50, 60]}
abc_optim = GridSearchCV(abc, parameters_abc)
abc_optim.fit(features, labels)
print 
print 'RandomForestClassifier():'
print abc_optim.best_params_
print
'''

# Re-run with optimized parameters
models = [GaussianNB(), AdaBoostClassifier(algorithm='SAMME.R',n_estimators=5,random_state=10),
          RandomForestClassifier(n_estimators=2,min_samples_split=6,min_samples_leaf=1)]
cv = StratifiedShuffleSplit(labels, n_iter = 100, test_size = 0.5, random_state = 10)
test_results = {}
for i in range(len(models)):
    clf = models[i]
    clf_str = re.split(r'\(', str(clf))[0]
    test_results[clf_str] = {}
    test_results[clf_str]['Accuracy'] = test_algorithm(clf,features,labels,'accuracy',cv)
    test_results[clf_str]['Precision'] = test_algorithm(clf,features,labels,'precision',cv)
    test_results[clf_str]['Recall'] = test_algorithm(clf,features,labels,'recall',cv)

### Plot results
df_results = pd.DataFrame.from_dict(test_results).T
ax = df_results.plot(kind='bar',figsize=(10,5),fontsize=12)
ax.set_title('Results of Different Models\n(Using Optimized Parameters)',fontsize=16)
ax.legend(bbox_to_anchor=(0.95, 0.9, .17, 0), loc=3, ncol=1, mode='expand', borderaxespad=0)
ax.text(.12,0.265,'Score > \n      0.3',fontsize=12,color='r')
ax.set_xlabel('Algorithm',fontsize=16)
ax.set_ylabel('Score Value',fontsize=16)
ax.plot([-.5, 6.5],[0.30, 0.30],'k--',linewidth=2)
plt.show()

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
features_list = top_features
clf = GaussianNB()
dump_classifier_and_data(clf, my_dataset, features_list)

### Test using class test
print
print
print 'Using Tester Script Provided for Project:'
print '========================================='
import tester
tester.main()
