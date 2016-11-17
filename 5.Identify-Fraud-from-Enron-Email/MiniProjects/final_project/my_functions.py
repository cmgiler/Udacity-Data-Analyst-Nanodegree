""" functions created to clean up poi_id code contains functions
	for both data-processing and plotting results
"""

from feature_format import featureFormat, targetFeatureSplit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict

def num_datapoints(data_dict):
	total_data_points = len(data_dict)
	count_poi = 0
	for person in data_dict:
		if data_dict[person]['poi'] == 1:
			count_poi += 1
	return total_data_points, count_poi


def num_features(data_dict):
	first_key = data_dict.keys()[0]
	features_count = len(data_dict[first_key].keys())
	data_types = defaultdict(list)
	for key in data_dict[first_key].keys():
		data_type = type(data_dict[first_key][key])
		data_types[data_type].append(key)

	return features_count, data_types

def num_nan_values(data_dict):
	### Count by feature:
	count_nan = defaultdict(int)
	first_key = data_dict.keys()[0]
	for key in data_dict[first_key].keys():
		count_nan[key] = 0
	for person in data_dict:
		for key in data_dict[person].keys():
			if isinstance(data_dict[person][key], str):
				if data_dict[person][key] == 'NaN':
					count_nan[key] += 1
			elif isinstance(data_dict[person][key], float):
				if np.isnan(data_dict[person][key]):
					count_nan[key] += 1

	### Count by person
	count_nan_ind = defaultdict(int)
	for person in data_dict:
		cnt = 0
		for key in data_dict[person].keys():
			if isinstance(data_dict[person][key], str):
				if data_dict[person][key] == 'NaN':
					cnt += 1
			elif isinstance(data_dict[person][key], float):
				if np.isnan(data_dict[person][key]):
					cnt += 1
		count_nan_ind[person] = cnt
	return count_nan, count_nan_ind


def remove_outliers(data_dict, outliers):
	for name in outliers:
		data_dict.pop(name)
	return data_dict


def preprocess_data(data_dict):
	# Convert to dataframe for easier processing
	df = pd.DataFrame.from_dict(data_dict, orient='index')
	df = df.replace('NaN',np.nan)
	df = df.drop('email_address', 1)

	# Convert NaN to Median Value of feature
	df = df.apply(lambda x: x.fillna(x.median()), axis=0)

	# Convert back to dict and return
	data_dict = df.T.to_dict()
	return data_dict


def add_features(data_dict, features_list):
	# Convert to dataframe for easier processing
	df = pd.DataFrame.from_dict(data_dict, orient='index')
	# Create new features
	# Fraction from poi
	
	df['fraction_from_poi'] = df['from_poi_to_this_person']/df['from_messages']
	features_list.append('fraction_from_poi')
	
	# Fraction to poi
	df['fraction_to_poi'] = df['from_this_person_to_poi']/df['to_messages']
	features_list.append('fraction_to_poi')

	# Convert back to dict and return
	data_dict = df.T.to_dict()
	return data_dict, features_list


def select_features(data_dict, features_list, select_count=10, 
					plot_results=True):
	data = featureFormat(data_dict, features_list, 
						 remove_NaN=False, sort_keys=True)
	labels, features = targetFeatureSplit(data)

	### Feature scaling
	from sklearn import preprocessing
	from sklearn.feature_selection import SelectKBest
	features = preprocessing.MinMaxScaler().fit_transform(features)

	### SelectKBest
	selection = SelectKBest(k = 'all')
	selection.fit(features, labels)
	scores = selection.scores_
	score_pairs = zip(features_list[1:], scores)
	score_pairs = sorted(score_pairs, key = lambda x: x[1])
	score_pairs.reverse()

	top_features = ['poi']
	for name, val in score_pairs:
	    if len(top_features) <= select_count:
	        top_features.append(name)

	if plot_results:
		# Plot score for each feature to new figure
		features_names = zip(*score_pairs)[0]
		score = zip(*score_pairs)[1]
		x_pos = np.arange(len(features_names)) 
		#plt.figure(figsize=(10,8))
		plt.figure()
		plt.barh(x_pos, score, align='center')
		plt.yticks(x_pos, features_names) 
		plt.ylabel('Score')
		plt.xlabel('Feature')
		plt.gca().invert_yaxis()
		#for i, v in enumerate(score):
		#    v = float("{0:.2f}".format(v))
		#    plt.text(v + .5, i+.25, str(v), color='blue', fontweight='bold')
		plt.show()

	return top_features, score_pairs


def rank_features(data_dict, features_list, plot_results=True):
	import operator
	from sklearn import metrics
	from sklearn.feature_selection import RFE
	from sklearn.ensemble import ExtraTreesClassifier
	from sklearn.linear_model import LogisticRegression

	# Reload data using only top 10 features found through K-Best Selection
	data = featureFormat(data_dict, features_list, sort_keys=True)
	labels, features = targetFeatureSplit(data)
	
	### Feature scaling
	from sklearn import preprocessing
	features = preprocessing.MinMaxScaler().fit_transform(features)

	# Create a base classifier used to evaluate a subset of attributes
	model = LogisticRegression()
	model_fi = ExtraTreesClassifier()

	# create the RFE model and select 10 attributes
	rfe = RFE(model, 1)
	rfe = rfe.fit(features, labels)

	# Use model_fi to find feature importance
	model_fi.fit(features, labels)
	feat_imp = model_fi.feature_importances_

	# Put rankings and feature importance values into a single dictionary
	# Keys = feature
	# Values = tuple - (feat_imp, ranking)
	ranking_dict = {}
	ranking = rfe.ranking_
	for i in range(len(ranking)):
	    ranking_dict[features_list[i+1]] = (feat_imp[i], ranking[i])
	ranking_pairs = zip(features_list[1:], feat_imp, ranking)
	ranking_pairs = sorted(ranking_pairs, key = lambda x: x[1])
	ranking_pairs.reverse()

	ranking_dict = sorted(ranking_dict.items(), key=operator.itemgetter(1))
	ranking_dict.reverse()
	
	if plot_results:
		# Show plot for feature importance and rankings
		features_names = zip(*ranking_pairs)[0]
		feature_importance = zip(*ranking_pairs)[1]
		feature_ranking = zip(*ranking_pairs)[2]
		x_pos = np.arange(len(features_names)) 

		plt.figure(figsize=(10,8))
		plt.barh(x_pos, feature_importance, align='center')
		plt.yticks(x_pos, features_names) 
		plt.ylabel('Feature Importance')
		plt.xlabel('Feature')
		plt.gca().invert_yaxis()
		for i, v in enumerate(feature_importance):
		    v = float("{0:.4f}".format(v))
		    if feature_ranking[i] == 1:
		        text_color = 'red'
		        text_weight = 'bold'
		    else:
		        text_color = 'blue'
		        text_weight = 'light'
		    plt.text(v + .001, i+.25, str(feature_ranking[i]),
		    		 color=text_color, fontweight=text_weight)
		        
		plt.show()

	return ranking_pairs


def test_algorithm(clf, features, labels, score_str, cv):
	from sklearn.cross_validation import cross_val_score
	return np.mean(cross_val_score(clf,features,labels,scoring=score_str,cv=cv))


def plot_df_results(df_results):
	ax = df_results.plot(kind='bar',figsize=(8,5),fontsize=12)
	ax.set_title('Results of Different Models\n(Using Default Settings)',fontsize=16)
	ax.legend(bbox_to_anchor=(0.95, 0.9, .17, 0), loc=3, ncol=1, mode='expand', borderaxespad=0)
	ax.text(-0.05,0.32,'Score > 0.3',fontsize=12,color='r')
	ax.set_xlabel('Algorithm',fontsize=16)
	ax.set_ylabel('Score Value',fontsize=16)
	ax.plot([-.5, 6.5],[0.30, 0.30],'k--',linewidth=2)
	plt.show()



