import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import Series
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split

#matplotlib inline

###########################################################
#----------------------------------------------01----------------------------------------------------------
# Loading Data-Set
label = pd.read_csv("secom_labels.txt", delim_whitespace=True, header=None)
print(label.info())
features = pd.read_csv("secom_data.txt", delim_whitespace=True,header=None)
print(features.info())

features = features.rename(columns={features.columns[i]: 'F'+ str(i) for i in range (590)}) # adding name to feature columns
label = label.rename(columns={0: 'L0', 1 :'date'})   # adding name to label column

############################################################

# Concatinating to separate files
df = pd.concat([features,label],axis=1, ignore_index=False)
#print(df.head()) # Preliminary inspection of data-set
#print(df.shape) # Preliminary inspection of data-set
#print(df.index) # Preliminary inspection of data-set

# Dropping columns with more than 10% missing data
df = df.dropna(thresh=len(df) - int(0.1 * len(df)), axis=1)
df = df.fillna(df.median())
df.L0.replace(-1,0, inplace=True) # Converting label column to binary [0,1]

# Building label vectore (y) and feature matrix(X)
y = df['L0']
X = df.drop(['L0','date'], axis=1)

#----------------------------------------------02----------------------------------------------------------
# Employing Lasso regularization approach to reduce feature matrix dimenssion
lasso = Lasso(alpha=0.2,normalize=False)
lasso_coef = lasso.fit(X, y).coef_
print('Total number of remaining features:')
print(len(lasso_coef[lasso_coef!=0.0]))

# Making a list from selected features
val = lasso_coef[lasso_coef!=0.0]
key, = np.where(lasso_coef!=0.0)
feature_list = X.columns[key]
val_plt = np.multiply(val,1000)
feature_list = feature_list.tolist()
print("featureList:",feature_list)
feature_column = key.tolist()
val = val.tolist()
print('List of selected features via Lasso dimenssion reduction:')
print(feature_list)

# revising feature matrix based on LASSO features reduction
X = X[feature_list]
print("X:",X)

#----------------------------------------------03----------------------------------------------------------

# Making correlation coefficients pair plot of all feature in order to identify degenrate features
plt.figure(figsize=(25,25))
df1 = pd.concat([X,y],axis=1, ignore_index=False)
ax = plt.axes()
corr = df1.corr()
sns.heatmap(corr, vmax=1,vmin=-1, square=True, annot=False, cmap='Spectral',linecolor="white", linewidths=0.01, ax=ax)
plt.xticks(rotation=90,fontweight="bold", size=15)
plt.yticks(rotation=0,fontweight="bold", size=15)
plt.title('Correlation Coefficient Pair Plot', fontweight="bold", size=18)
plt.savefig('pcp.png')
plt.show()

# Making box plot to explore features variations and outliers
plt.figure(figsize=(16,8))
sns.set()
sns.boxplot(data=X, orient="v", palette="Set2")
plt.xlabel('Features',fontweight="bold", size=12)
plt.ylabel('Variation',fontweight="bold", size=12)
plt.title('Box Plot of Selected Features', fontweight="bold", size=18)
plt.yscale('symlog', nonposy='clip')
plt.xticks(rotation=90)
plt.savefig('BoxPlot.png');plt.show()

# Exploratory Data Analysis
# Plotting total products against failed product in histogram format
bins = 30
for feature in feature_list:
    tf = feature
    plt.figure()
    plt.hist(df1[tf], bins = bins, color='m',label = 'Total',alpha=0.5)
    plt.hist(df1[tf][df1['L0'] == 1], bins = bins, color='b',label = 'Fail')

    plt.xlabel(tf);plt.ylabel('Production')
    plt.title('Feature ID:'+tf,fontweight="bold", size=12)
    plt.yscale('log')

    plt.legend();plt.savefig(tf+'.png');
    plt.close();

#----------------------------------------------04----------------------------------------------------------
# Statistical Analysis & Hypothesis Testing
num_replica = 3000
bs_replica = np.empty(num_replica)
ht_feature = 'F484'
threshold = 680

lower_range = df1[(df1[ht_feature] > threshold)]
higher_range = df1[(df1[ht_feature] <= threshold)]

lower_range_ratio = len(lower_range[lower_range['L0'] == 1]) / len(lower_range)
higher_range_ratio = len(higher_range[higher_range['L0'] == 1]) / len(higher_range)
ratio_diff = higher_range_ratio - lower_range_ratio

print('Higher fail ratio:', "%.3f" % higher_range_ratio)
print('Lower fail ration:', "%.3f" % lower_range_ratio)
print('Ratio difference:', "%.3f" % ratio_diff)

# Bootstrapping
for i in range(num_replica):
    lr_bs = lower_range.sample(frac=1, replace=True)
    hr_bs = higher_range.sample(frac=1, replace=True)

    lr_bs_r = len(lr_bs[lr_bs['L0'] == 1]) / len(lr_bs)
    hr_bs_r = len(hr_bs[hr_bs['L0'] == 1]) / len(hr_bs)
    ratio_diff_bs = hr_bs_r - lr_bs_r
    bs_replica[i] = ratio_diff_bs

# Histogram plot
plt.hist(bs_replica, bins=20)
plt.axvline(ratio_diff, color='r', linestyle='dashed', linewidth=3)
plt.xlabel('Yield Ratio Difference', fontweight="bold", size=12)
plt.savefig('Hypothesis.png');
plt.show()

# Calculating P-value
print('Mean ratio decrease:', "%.3f" % np.mean(bs_replica))
print('95% Confidence interval:', (np.percentile(bs_replica, [2.5, 97.5])))
print('P-value:', np.sum(bs_replica > (ratio_diff)) / num_replica)

#----------------------------------------------05----------------------------------------------------------
# Preparing data for time series analysis
# Concatinating two separate files
df2 = pd.concat([features,label],axis=1, ignore_index=False)

# Converting to time series format
df2.date = pd.to_datetime(df2.date)
df2.set_index('date', inplace=True)

# Resampling yield data based on daily information
failed_product = df2.L0[df2['L0']==1].resample('D').count()
total_product = df2.L0[df2['L0']==-1].resample('D').count()

failed_ratio = failed_product * 100 / total_product
failed_ratio = failed_ratio.dropna()

# Visualizaion of daily production failed ratio
sns.set()

failed_ratio.plot(style='bo-',MarkerSize=4, LineWidth = 0.6, figsize=(15,5))

plt.xlabel('Date', fontweight="bold", size=12)
plt.ylabel('Failed Ratio (%)', fontweight="bold", size=12)
plt.grid(True);plt.savefig('100Days.png')
plt.show()

# Indexing dates with more than 50% failed ratio
date_index = failed_ratio[failed_ratio >= 50]

# Plotting F484 for date_index
df2['F484'].loc['2008-07-21'].hist(alpha=0.7, label = '2008-07-21')
df2['F484'].loc['2008-07-29'].hist(alpha=0.7, label = '2008-07-29')
df2['F484'].loc['2008-07-30'].hist(alpha=0.7, label = '2008-07-30')
df2['F484'].loc['2008-10-08'].hist(alpha=0.7, label = '2008-10-08')
plt.axvline(680, color='r', linestyle='dashed', linewidth=3) # Thresold in hypothesis testing (Previouse section)
plt.xlabel('F484', fontweight="bold", size=12)
plt.legend()
plt.savefig('F484_Worst.png')
plt.show()

#----------------------------------------------06----------------------------------------------------------
#########################################################
# Claculating default Ratio
passed = len(df[df['L0']==0])
failed = len(df[df['L0']==1])
ratio = float(failed/(passed+failed))
print('Number of passed sample:', passed)
print('Number of failed sample:', failed)
print('Default Ratio (failed/total) :', "%.3f" % ratio)

#########################################################
# Splitting data to train and test sets

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.3, random_state=42)
X_test = X_test.as_matrix() # Coverting dataframe to matrix for compatibility purpose

# Under-sampling of overer-represented calss (pass)
from imblearn.under_sampling import RandomUnderSampler
rus = RandomUnderSampler(random_state=0)
X_us, y_us = rus.fit_sample(X_train, y_train)

print('########################################')
print('Size of training data-set:', X_train.shape)
print('Size of under sampling data_set:', X_us.shape)

# Over-sampling of under-represented calss (fail)
from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=0)
X_os, y_os = ros.fit_sample(X_train, y_train)
print('Size of overer sampling data_set:', X_os.shape)


#——————————————————————————————————————————————————————————————————————————————


from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import numpy as np
import warnings

warnings.filterwarnings('ignore')

knn = KNeighborsClassifier()#Obtain KNN classifier
#Set the range of k
k_range = list(range(1,10))
leaf_range = list(range(1,2))
weight_options = ['uniform','distance']
algorithm_options = ['auto','ball_tree','kd_tree','brute']
param_gridknn = dict(n_neighbors = k_range,weights = weight_options,algorithm=algorithm_options,leaf_size=leaf_range)
gridKNN = GridSearchCV(knn,param_gridknn,cv=10,scoring='accuracy',verbose=1)
g=gridKNN.fit(X_train,y_train)
print(g)
print('best score is:',str(gridKNN.best_score_))
print('best params are:',str(gridKNN.best_params_))
joblib.dump(gridKNN, "knn.mode")
c=joblib.load("knn.mode")
dtrain_predictions = c.predict(X)
np.savetxt("knn.txt", dtrain_predictions, fmt="%d", delimiter=",")
print(list())
np.savetxt("test.txt", y, fmt="%d", delimiter=",")