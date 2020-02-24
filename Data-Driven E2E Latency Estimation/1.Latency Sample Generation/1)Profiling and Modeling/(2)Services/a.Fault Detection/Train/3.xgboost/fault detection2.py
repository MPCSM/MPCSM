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

import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
from sklearn.metrics import roc_curve, auc,roc_auc_score
from sklearn.metrics import classification_report
from matplotlib.pylab import rcParams
import warnings
warnings.filterwarnings('ignore')
rcParams['figure.figsize'] = 12, 4


# XGB Model

def xgb_model(alg, X_matrix, y_vector, test_matrix, test_vector, useTrainCV=True, useTestSet=False, cv_folds=5,
              early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(X_matrix, y_vector)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
                          metrics='auc', early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])

    # Fit the algorithm on the data
    alg.fit(X_matrix, y_vector, eval_metric='auc')
    alg.get_booster().save_model('xgb.model')
    #tar = xgb.Booster(model_file='xgb.model')
    #alg.save_model('0001.model')
    # Predict training set:
    dtrain_predictions = alg.predict(X_matrix)
    print("dtrain:",dtrain_predictions)
    print("test:",y_vector)

xgb2 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=200,
 max_depth=6,
 min_child_weight=14,
 gamma=0.4,
 subsample=0.8,
 colsample_bytree=0.75,
 reg_alpha=0.5,
 reg_lambda=1,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)
xgb_model(xgb2, X_train, y_train, X_test, y_test, useTestSet = True)




