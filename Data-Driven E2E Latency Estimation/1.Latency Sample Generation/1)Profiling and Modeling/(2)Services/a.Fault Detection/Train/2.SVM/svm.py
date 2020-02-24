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

#----------------------------------------------04----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.3, random_state=42)
X_test = X_test.as_matrix() # Coverting dataframe to matrix for compatibility purpose
#----------------------------------------------07----------------------------------------------------------
# Import ML Libraries

import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV

import numpy as np
import sklearn.model_selection as ms
import sklearn.svm as svm
import sklearn.metrics as sm
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.metrics import accuracy_score
from matplotlib import pyplot
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import sklearn.metrics as sm
import warnings
import sklearn.model_selection as ms
warnings.filterwarnings('ignore')
svc = SVC()
parameters = [
    {
        'C': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
        'gamma': [0.00001, 0.0001, 0.001, 0.1, 1, 10, 100, 1000],
        'kernel': ['rbf']
    },
    #{
      #  'C': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
        #'kernel': ['linear']
  #  }
]
clf = GridSearchCV(svc, parameters, cv=5, n_jobs=8)
c=clf.fit(X_train, y_train)
print(clf.best_params_)
best_model = clf.best_estimator_
best_model.predict(X_test)
accuracy = c.score(X_test, y_test)
print("accuracy:{}".format(accuracy))
joblib.dump(c, "SVM.model")
d= joblib.load("SVM.model")
dtrain_predictions = d.predict(X)
np.savetxt("svm.txt", dtrain_predictions, fmt="%d", delimiter=",")
