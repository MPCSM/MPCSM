# best : {'gamma': 0.0, 'learning_rate': 0.0525255663562885, 'max_depth': 11, 'min_child_weight': 2, 'n_estimators': 209, 'subsample': 0.8}
# best param after transform :
# {'gamma': 0.0, 'learning_rate': 0.05105051132712577, 'max_depth': 16, 'min_child_weight': 3, 'n_estimators': 359, 'subsample': 0.5800000000000001}
# rmse of the best xgboost: 46.86753444802549

import matplotlib

# Force matplotlib to not use any Xwindows backend.

matplotlib.use('Agg')
from hyperopt import fmin, tpe, hp, partial
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, zero_one_loss
from sklearn.metrics import log_loss
import xgboost as xgb
import pandas as pd
from xgboost import plot_importance
from matplotlib import pyplot as plt
totalcount=10

#----------------------------------------------01----------------------------------------------------------

attribute = pd.read_csv(str(totalcount)+'-mix-three-data-1.csv')
label = pd.read_csv(str(totalcount)+'-mix-three-label.csv')
#print(waferA.info())
#print(waferL.info())

#mapping_type={'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}
# print(1)
label=label['totalLatency']
# print(1)
attribute=attribute.loc[:,~attribute.columns.str.contains('^Unnamed')]

#print(waferlabel)
# Download the data and split into training and test sets
X=attribute
#print(X)

y=label
# print(y.dtypes)
# print(X.dtypes)
# print(np.isnan(X))
# print(111)
# print(np.isnan(y).any())
# print(np.isfinite(X.all()))
# # X= X.fillna(0)
# y = y.fillna(0)
#y.to_csv("THREE.csv")
############################################################
#----------------------------------------------04----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2, random_state=42)


dtrain = xgb.DMatrix(data=X_train,label=y_train,missing=-999.0)
dtest = xgb.DMatrix(data=X_test,label=y_test,missing=-999.0)
DATA=xgb.DMatrix(data=X,label=y,missing=-999.0)
evallist = [(dtest, 'eval'), (dtrain, 'train')]

space = {"max_depth": hp.randint("max_depth", 15),
         "n_estimators": hp.randint("n_estimators", 300),
         'learning_rate': hp.uniform('learning_rate', 1e-3, 5e-1),
         'gamma': hp.randint('gamma', 5),
         "subsample": hp.randint("subsample", 5),
         "min_child_weight": hp.randint("min_child_weight", 6),
         }
#------------------------------------------------------------03------------------------------


def argsDict_tranform(argsDict, isPrint=False):
    argsDict["max_depth"] = argsDict["max_depth"] + 5
    argsDict["gamma"] = argsDict["gamma"] *0.1
    argsDict['n_estimators'] = argsDict['n_estimators'] + 150
    argsDict["learning_rate"] = argsDict["learning_rate"] * 0.02 + 0.05
    argsDict["subsample"] = argsDict["subsample"] * 0.1 + 0.5
    argsDict["min_child_weight"] = argsDict["min_child_weight"] + 1
    if isPrint:
        print(argsDict)
    else:
        pass

    return argsDict
#------------------------------------------------------05----------------
def xgboost_factory(argsDict):
    argsDict = argsDict_tranform(argsDict)

    params = {'nthread': -1,  
              'max_depth': argsDict['max_depth'], 
              'n_estimators': argsDict['n_estimators'],  
              'eta': argsDict['learning_rate'],  
              'subsample': argsDict['subsample'],  
              'min_child_weight': argsDict['min_child_weight'],  
              #'objective': 'reg:linear',
              'silent': 0,  
              'gamma': 0,  
              'colsample_bytree': 0.7,  
              'alpha': 0,  
              'lambda': 0,  
              'scale_pos_weight': 0,  
              'seed': 100,  
              'missing': -999,  
              }
    params['eval_metric'] = ['rmse']

    xrf = xgb.train(params, dtrain, params['n_estimators'], evallist, early_stopping_rounds=200)
    joblib.dump(xrf, str(totalcount)+'-mix-threexgboost-1.pkl')
    plot_importance(xrf)
    plt.subplots_adjust(left=0.30, wspace=0.25, hspace=0.25,
                        bottom=0.13, top=0.91)
    plt.savefig(str(totalcount)+"-mix-threexgboost-1.png")
    plt.show()
    return get_tranformer_score(xrf)


def get_tranformer_score(tranformer):
    xrf = tranformer
    dpredict = xgb.DMatrix(X_test)
    prediction = xrf.predict(dpredict, ntree_limit=xrf.best_ntree_limit)

    return mean_squared_error(y_test, prediction)

#------------------------------------------06-------------------
algo = partial(tpe.suggest, n_startup_jobs=1)
best = fmin(xgboost_factory, space, algo=algo, max_evals=100, pass_expr_memo_ctrl=None)

#------------------------------------07------------
RMSE = xgboost_factory(best)
print('best :', best)
print('best param after transform :')
argsDict_tranform(best,isPrint=True)
print('rmse of the best xgboost:', np.sqrt(RMSE))
#

# # #
# d= joblib.load('threexgboost.pkl')
#
# y= d.predict(DATA)
# np.savetxt("THREE.txt", y, fmt="%d", delimiter=",")