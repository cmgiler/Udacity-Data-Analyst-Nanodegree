#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

'''
count = 0
for person in enron_data.keys():
	if enron_data[person]['poi'] == 1:
		count += 1

print count
'''

#print enron_data['PRENTICE JAMES']['total_stock_value']

#print enron_data['COLWELL WESLEY']['from_this_person_to_poi']

#print enron_data['SKILLING JEFFREY K']['exercised_stock_options']

'''
keylist = enron_data.keys()
keylist.sort()
for key in keylist:
    print "%s: %s" % (key, enron_data[key]['total_payments'])
'''

count_salary = 0
count_email = 0
for key in enron_data:
    if enron_data[key]['salary'] != 'NaN':
        count_salary += 1
    if enron_data[key]['email_address'] != 'NaN':
        count_email += 1

print "%s folks with quantified salary; %s folks with known email address" % (count_salary, count_email)
