from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.externals import joblib
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
import os.path
# nano 0,laptop 1,miniserver 2,cloud 3
microNames=["wafer-static","fault-losso","wafer-auto","rul-preprocess","rul-prediction","wafer-cnn","fault-knn",
            "wafer-svm","fault-svm","fault-xgboost","wafer-ensemble","fault-ensemble"]
devices=[0,1,2,3]
datasums=[10,20,30,40,50,60,70,80]
deggs=[]
models=[]
for microName in microNames:

    for device in devices:

        for datasum in datasums:
            print(microName, device,datasum)
            datafile="data/"+str(microName) + '-' + str(device) +"-"+ str(datasum)+ '.csv'
            if(os.path.isfile(datafile)):
                data = pd.read_csv(datafile)
                X=data["CpuPercent"].values
                X = X[:, np.newaxis]
                y=data['Latency'].values
                y=y[:, np.newaxis]
                # ############################################################
                # # #----------------------------------------------04----------------------------------------------------------
                X, X_test, y, y_test = train_test_split(X, y,test_size = 0.3, random_state=42)

                dstfile="finallyResult/"+str(microName) + '-' + str(device+2) +  "-"+str(datasum)+'.m'

                for deg in range(2,11):
                    quadratic_featurizer = PolynomialFeatures(degree=deg)
                    X_train_quadratic = quadratic_featurizer.fit_transform(X)
                    regressor_model = LinearRegression()
                    regressor_model.fit(X_train_quadratic, y)
                    joblib.dump(regressor_model, str(deg)+"_poly.m")

                score=-float('inf')

                for deg in range(2,11):
                    X_test = [[250], [300]]  
                    y_test = [[310], [330]]
                    regressor_model=joblib.load(str(deg)+"_poly.m")
                    quadratic_featurizer = PolynomialFeatures(degree=deg)
                    X_test_quadratic = quadratic_featurizer.fit_transform(X_test)
                    thiscore=regressor_model.score(X_test_quadratic, y_test)
                    
                    if(thiscore>score):
                        degg=deg
                        themodel=str(deg)+"_poly.m"
                        score=thiscore
                models.append([dstfile,degg])
                shutil.move(themodel,dstfile)

attribute=['models','deg']
addressPD=pd.DataFrame(columns=attribute,data=models)
addressPD.to_csv("finallyResult/map.csv")

from sklearn.externals import joblib
import pandas as pd
modelfile="Polynomial/finallyResult/" + "wafer-static" + '-' + "4" + "-" + str(10) + '.m'
regressor_model=joblib.load(str(deg)+"_poly.m")
themap = pd.read_csv("finallyResult/map.csv")
test=themap.ix[modelfile]
print(test)

