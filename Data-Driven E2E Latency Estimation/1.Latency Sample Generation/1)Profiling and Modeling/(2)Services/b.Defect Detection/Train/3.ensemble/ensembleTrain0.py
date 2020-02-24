
'''
96.1%
ExtraTreesClassifier(bootstrap=True, class_weight=None, criterion='gini',
                     max_depth=None, max_features=None, max_leaf_nodes=None,
                     min_impurity_decrease=0.0, min_impurity_split=None,
                     min_samples_leaf=1, min_samples_split=2,
                     min_weight_fraction_leaf=0.0, n_estimators=905, n_jobs=1,
                     oob_score=False, random_state=2, verbose=False,
                     warm_start=False)

'''
from hpsklearn import HyperoptEstimator, any_regressor, any_preprocessing,any_classifier
from hyperopt import tpe
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


wafer=pd.read_csv("waferAttribute0.csv")
waferlabel=pd.read_csv("waferResult.csv")
mapping_type={'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}

waferlabel=waferlabel['result']

wafer=pd.DataFrame(wafer,columns=['cnnResult','svmResult'])
print(wafer.info())
print(wafer[:2])


# Download the data and split into training and test sets


X=wafer.values
print(X[:2])

y=waferlabel.values
print(y[:2])

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
joblib.dump(estim,'ensemble0.m')

#ensemble=joblib.load('ensemble0.m')

estim.predict(X_test)


