
### Step 1: Choose Your Data Set
Titanic Data (from Kaggle website). Contains demographics and passenger information from 891 of the 2224 passengers and crew on board the Titanic.

### Step 2: Get Organized
Package includes:
 - iPython Notebook Report (HTML Format)
 - iPython Notebook (ipynb Format)

Data Used:
 - titanic_data.csv


```python
# Install Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
```


```python
# Load CSV file into DataFrame
titanic_df = pd.read_csv('titanic_data.csv')
titanic_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
  </tbody>
</table>
</div>



### Step 3/4: Analyze Your Data & Share Your Findings
This project seeks to answer the following questions:
 - What type of passengers were on-board the Titanic (Gender, Age, Class)?
 - How does a passenger's class relate to which deck he/she is on?
 - How many families were on-board (vs. passengers traveling alone)?
 - What factors made more people likely to survive?*
 
*It should be noted that these findings are tentative, and will require further statistical analysis to ensure their validity


```python
# Gender Breakdown
sns.factorplot(x = 'Pclass',data=titanic_df, kind = 'count', hue = 'Sex')
```




    <seaborn.axisgrid.FacetGrid at 0x24c72fd0>




![png](output_5_1.png)


Most passengers were in 3rd class. While the count of male and female passengers for the first two classes are fairly similar, 3rd class contained almost double the number of male than female passengers.

This does not take into account the passengers' ages, so further analysis is conducted to separate children from adult passengers


```python
# Create New Category - Find children (age <= 16 y.o.)
def find_child(passenger):
    age, sex = passenger
    if age <= 16:
        return 'child'
    else:
        return sex
    
# Apply to DataFrame to add new column
titanic_df['PersonType'] = titanic_df[['Age', 'Sex']].apply(find_child, axis = 'columns')
titanic_df[0:10]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
      <th>PersonType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>NaN</td>
      <td>S</td>
      <td>male</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
      <td>female</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>NaN</td>
      <td>S</td>
      <td>female</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
      <td>female</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>NaN</td>
      <td>S</td>
      <td>male</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>0</td>
      <td>3</td>
      <td>Moran, Mr. James</td>
      <td>male</td>
      <td>NaN</td>
      <td>0</td>
      <td>0</td>
      <td>330877</td>
      <td>8.4583</td>
      <td>NaN</td>
      <td>Q</td>
      <td>male</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>0</td>
      <td>1</td>
      <td>McCarthy, Mr. Timothy J</td>
      <td>male</td>
      <td>54</td>
      <td>0</td>
      <td>0</td>
      <td>17463</td>
      <td>51.8625</td>
      <td>E46</td>
      <td>S</td>
      <td>male</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>0</td>
      <td>3</td>
      <td>Palsson, Master. Gosta Leonard</td>
      <td>male</td>
      <td>2</td>
      <td>3</td>
      <td>1</td>
      <td>349909</td>
      <td>21.0750</td>
      <td>NaN</td>
      <td>S</td>
      <td>child</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>1</td>
      <td>3</td>
      <td>Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)</td>
      <td>female</td>
      <td>27</td>
      <td>0</td>
      <td>2</td>
      <td>347742</td>
      <td>11.1333</td>
      <td>NaN</td>
      <td>S</td>
      <td>female</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>1</td>
      <td>2</td>
      <td>Nasser, Mrs. Nicholas (Adele Achem)</td>
      <td>female</td>
      <td>14</td>
      <td>1</td>
      <td>0</td>
      <td>237736</td>
      <td>30.0708</td>
      <td>NaN</td>
      <td>C</td>
      <td>child</td>
    </tr>
  </tbody>
</table>
</div>




```python
sns.factorplot('Pclass', data=titanic_df, hue='PersonType', kind='count')
print 'Counts of Passenger Type'
print titanic_df['PersonType'].value_counts()
```

    Counts of Passenger Type
    male      526
    female    265
    child     100
    Name: PersonType, dtype: int64



![png](output_8_1.png)


A high proportion of the children on-board the Titanic were in 3rd class.


```python
print "The average age of people on-board the titanic (based on the given sample of %d passengers) was: %2.2f years." % \
(titanic_df['PassengerId'].max(), titanic_df['Age'].mean())
plt.figure()
titanic_df['Age'].hist()
plt.title('Age Distribution of Titanic Passengers')
plt.xlabel('Age (years)')
plt.ylabel('Count (# of Passengers)')
```

    The average age of people on-board the titanic (based on the given sample of 891 passengers) was: 29.70 years.





    <matplotlib.text.Text at 0x24c2ca90>




![png](output_10_2.png)



```python
# Finding the differences in mean Age and Fare by Passenger Class
titanic_df.groupby('Pclass').mean()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Fare</th>
    </tr>
    <tr>
      <th>Pclass</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>461.597222</td>
      <td>0.629630</td>
      <td>38.233441</td>
      <td>0.416667</td>
      <td>0.356481</td>
      <td>84.154687</td>
    </tr>
    <tr>
      <th>2</th>
      <td>445.956522</td>
      <td>0.472826</td>
      <td>29.877630</td>
      <td>0.402174</td>
      <td>0.380435</td>
      <td>20.662183</td>
    </tr>
    <tr>
      <th>3</th>
      <td>439.154786</td>
      <td>0.242363</td>
      <td>25.140620</td>
      <td>0.615071</td>
      <td>0.393075</td>
      <td>13.675550</td>
    </tr>
  </tbody>
</table>
</div>



As expected, the average fare cost for 1st class is markedly higher (around 4x the cost of 2nd class on average). The average age is also noticably higher for 1st class passengers, as is the survival rate. This will be analyzed further later in this report


```python
deck = titanic_df['Cabin']
levels = []
omit_count = 0
for level in deck:
    if isinstance(level, str):
        levels.append(level[0])
    else:
        levels.append('Empty')
        omit_count += 1
        
cabin_df = pd.DataFrame(levels)
cabin_df.columns = ['Cabin_Deck']
sns.factorplot('Cabin_Deck', data=cabin_df, kind='count', palette='autumn_d', order=['A','B','C','D','E','F','G'])
titanic_df_cabin = pd.concat([titanic_df, cabin_df], axis=1)
sns.factorplot('Cabin_Deck', data=titanic_df_cabin, kind='count', hue='Pclass', order=['A','B','C','D','E','F','G'], \
               hue_order=[1,2,3],size=4, aspect=3)
print '%d lines of data have been omitted for missing values on Cabin listing' % omit_count
```

    687 lines of data have been omitted for missing values on Cabin listing



![png](output_13_1.png)



![png](output_13_2.png)


The most populated level was the C-Deck. Decks A, B, and C also contained only 1st-class passengers.


```python
# Identifying unlisted cabin data
sns.factorplot('Cabin_Deck', data=titanic_df_cabin, kind='count', hue='Pclass', order=['A','B','C','D','E','F','G','Empty'], \
               hue_order=[1,2,3],size=4, aspect=3)
average_fare = titanic_df_cabin.groupby('Cabin_Deck').mean()[['Fare']]
average_fare.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x246c67f0>




![png](output_15_1.png)



![png](output_15_2.png)


#### Note on omitted data:
Note that a large chunk of data has been omitted (almost 80% of all data), as Cabin information is not given for every line item. The plot above shows the number of passengers in each class with no listed cabin, compared to those in cabins A-G.

There seems to be a significant portion of 2nd and 3rd class passengers with an unlisted cabin. The second figure shows the average fare for passengers with an unlisted cabin ('Empty') is fairly similar to those in the lower cabin decks (F and G). However, we can not be sure of the actual meaning of these unlisted items. For this reason, they have been omitted from the previous analysis.


```python
##### Calculated the average fare cost and age per Cabin Deck
average_fare_age = titanic_df_cabin.groupby('Cabin_Deck').mean()[['Age', 'Fare']]
average_fare_age.drop(['Empty','T'], inplace=True)
average_fare_age.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x239626a0>




![png](output_17_1.png)


There appears to be a clear correlation between Cabin Deck location and fare price, with fare cost decreasing as cabin level decreases (Deck A is Upper Promenade, while G is the Lower Deck). However, Cabin Deck A shows a much lower fare cost than Deck B. This could be explained by looking more closely at the floorplan (Cabins on Deck A are significantly smaller than those on Decks B and C).

URL for Titanic Deckplans: http://www.encyclopedia-titanica.org/titanic-deckplans/a-deck.html


```python
# Who were traveling alone vs. with family
titanic_df['Alone'] = titanic_df.SibSp + titanic_df.Parch
titanic_df['Alone'].loc[titanic_df['Alone'] > 0] = 'With Family'
titanic_df['Alone'].loc[titanic_df['Alone'] == 0] = 'Alone'
```


```python
sns.factorplot('Alone', data=titanic_df, kind='count')
```




    <seaborn.axisgrid.FacetGrid at 0x246b0400>




![png](output_20_1.png)



```python
# Determine which factors led to passenger survival
titanic_df['Survivor'] = titanic_df['Survived'].map({0:'no',1:'yes'})
titanic_df_cabin['Survivor'] = titanic_df_cabin['Survived'].map({0:'no',1:'yes'})
sns.factorplot('Survivor', data=titanic_df, kind='count', palette='winter_d', order=['no', 'yes'])
print 'The mean survival rate was %2.1f%% for the given set of data' % ((titanic_df['Survived'].mean())*100)
```

    The mean survival rate was 38.4% for the given set of data



![png](output_21_1.png)



```python
# Check class as a factor for survival rate
sns.factorplot(x='Pclass', y='Survived', data=titanic_df)
sns.factorplot(x='Pclass', y='Survived', data=titanic_df, hue='PersonType', hue_order=['child','female','male'])
titanic_df.groupby(['Pclass','PersonType']).mean()['Survived']
```




    Pclass  PersonType
    1       child         0.888889
            female        0.977273
            male          0.352941
    2       child         0.904762
            female        0.909091
            male          0.082474
    3       child         0.400000
            female        0.486486
            male          0.119355
    Name: Survived, dtype: float64




![png](output_22_1.png)



![png](output_22_2.png)


Survival rate was very much dependent on fare class (1st class passengers had a much higher survival rate than 2nd, and 2nd was much higher than 3rd).

Additionally, children and female passengers had a much higher survival rate than male survivors, with the greatest difference observed in 2nd class (male 2nd class passengers had a survival rate of around 8%, while women and children in the same class had a survival rate of approx. 90%).


```python
# Plotting by age and class
sns.lmplot('Age','Survived',data=titanic_df,hue='Pclass')
sns.lmplot('Age','Survived',data=titanic_df,hue='Sex')
```




    <seaborn.axisgrid.FacetGrid at 0x24671358>




![png](output_24_1.png)



![png](output_24_2.png)


As the first figure shows, survival rate in general decreased with age and with passenger class. However, there is much more variation in survival rate for older passengers.

The second figure shows that survival rate increased with age for women, while decreasing with age for men.


```python
sns.factorplot('Alone', data=titanic_df, hue='Survivor', kind='count', palette='Set1',hue_order=['no','yes'])
sns.factorplot('Cabin_Deck', data=titanic_df_cabin, hue='Survivor', kind='count', x_order = ['A','B','C','D','E','F','G'], \
              palette='Set1', size=4, aspect=3)
```




    <seaborn.axisgrid.FacetGrid at 0x257d50b8>




![png](output_26_1.png)



![png](output_26_2.png)


Passengers had a better chance of surviving if with family vs. if alone. Also, survival rate was highest for upper-level cabin decks. This is to be expected, as these decks were reserved for 1st-class passengers, who also had a higher overall survival rate.

### Conclusions / Discussion
The following conclusions were found in this study:
 - Passengers with family had a better survival rate than those traveling alone.
 - Being in a higher passenger class gave a better survival rate
 - Gender and Age also played a major role in survival (women and children had a much higher survival rate than men, regardless of passenger class)
 
#### Notes: 
 - This data does not contain all passengers on-board, so the actual case could be somewhat different from the conclusions drawn based on this sample of data. Statistical testing is needed to determine the confidence level of the conclusions drawn from this data sample.
 - Also, we cannot draw valid conclusions on passenger survival rates based on cabin location, because the majority of the data did not have this information listed. All figures above based on cabin deck have omitted this data.

### Resources used to complete this project:
 - Tutorials and Forums
    - http://stackoverflow.com/
    - https://stanford.edu/~mwaskom/software/seaborn/tutorial.html
    - http://chrisalbon.com/#Python
    - http://matplotlib.org/users/pyplot_tutorial.html
    - https://github.com/jmportilla/Udemy-notes
 - Background Information
    - http://www.encyclopedia-titanica.org/titanic-deckplans/
    - http://www.dummies.com/how-to/content/suites-and-cabins-for-passengers-on-the-titanic.html


```python

```


```python

```
