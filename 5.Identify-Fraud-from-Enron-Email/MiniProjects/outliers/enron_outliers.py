#!/usr/bin/python

import pickle
import sys
import matplotlib.pyplot as plt
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


### read in data dictionary, convert to numpy array
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
features = ["salary", "bonus"]
data_dict.pop('TOTAL',0)
data = featureFormat(data_dict, features)


### your code below

for point in data:
	salary = point[0]
	bonus = point[1]
	plt.scatter(salary, bonus)
plt.xlabel('salary')
plt.ylabel('bonus')
plt.show()

'''
keys = data_dict.keys()
keys.sort()
for key in keys:
	print key
'''