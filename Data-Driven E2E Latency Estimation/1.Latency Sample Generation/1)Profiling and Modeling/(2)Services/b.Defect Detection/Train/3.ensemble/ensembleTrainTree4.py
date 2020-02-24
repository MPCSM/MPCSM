from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import pandas as pd

wafer=pd.read_csv("waferAttribute4.csv")
waferlabel=pd.read_csv("waferResult.csv")
mapping_type={'Center':0,'Donut':1,'Edge-Loc':2,'Edge-Ring':3,'Loc':4,'Random':5,'Scratch':6,'Near-full':7,'none':8}

waferlabel=waferlabel['result']
wafer=pd.DataFrame(wafer,columns=['cnnResult','svmResult'])


# Download the data and split into training and test sets


X=wafer.values

y=waferlabel.values

X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.25, random_state=1)

model = ExtraTreesClassifier(bootstrap=True, class_weight=None, criterion='gini',
                     max_depth=None, max_features=None, max_leaf_nodes=None,
                     min_impurity_decrease=0.0, min_impurity_split=None,
                     min_samples_leaf=1, min_samples_split=2,
                     min_weight_fraction_leaf=0.0, n_estimators=905, n_jobs=1,
                     oob_score=False, random_state=2, verbose=False,
                     warm_start=False)
model.fit(X, y)
print(model.score(X_test,y_test))
joblib.dump(model,'ensembleTree4.m')
