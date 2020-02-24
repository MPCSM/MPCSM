
'''
0.9616309727554466 {'learner': ExtraTreesClassifier(bootstrap=True, class_weight=None, criterion='gini',
                     max_depth=None, max_features=None, max_leaf_nodes=None,
                     min_impurity_decrease=0.0, min_impurity_split=None,
                     min_samples_leaf=1, min_samples_split=2,
                     min_weight_fraction_leaf=0.0, n_estimators=905, n_jobs=1,
                     oob_score=False, random_state=2, verbose=False,
                     warm_start=False), 'preprocs': (MinMaxScaler(copy=True, feature_range=(-1.0, 1.0)),), 'ex_preprocs': ()}
'''
"""0.9872448979591837 {'preprocs': (), 'learner': AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
                   learning_rate=0.05368617271410339, n_estimators=883,
                   random_state=4), 'ex_preprocs': ()}"""
from hpsklearn import HyperoptEstimator, any_regressor, any_preprocessing,any_classifier
from hyperopt import tpe
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import  numpy as np
import xgboost as xgb

new_col=['xgbResult','knnResult','svmResult']
wafer=pd.read_csv("data.csv", names = new_col, header=0)
waferlabel=pd.read_csv("test.csv")

#mapping_type={'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}




#waferlabel=waferlabel['result']
#wafer=pd.DataFrame(wafer,columns=['xgbResult','knnResult','svmResult'])


# Download the data and split into training and test sets


X=wafer.values

y=waferlabel.values


X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.25, random_state=1)

estim = HyperoptEstimator(
        preprocessing=any_preprocessing('pp'),
        classifier=any_classifier('clf'),
        algo=tpe.suggest,
        trial_timeout=200.0,  # seconds
        max_evals=10,
        seed=1
    )

estim.fit( X_train, y_train )

print(estim.score(X_test, y_test),estim.best_model() )

joblib.dump(estim,'ensemble4.m')

ensemble=joblib.load('ensemble4.m')

ensemble.predict(X_test)


