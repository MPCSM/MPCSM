export decision=decision45
192.168.0.86
export lossoVolumes=/home/ljr/code/fault/losso:/exp
export lossoPubIp1=192.168.0.86
export lossoPubIp2=192.168.0.86
export lossoPubIp3=192.168.0.190
export lossoSubIp=192.168.0.86
export lossoCpu=7,8
export knnVolumes=/home/ljr/code/fault/knn:/exp
export knnPubIp=192.168.0.190
export knnSubIp=192.168.0.86
export knnCpu=5,6
export svmVolumes=/home/ljr/code/fault/svm:/exp
export svmPubIp=192.168.0.190
export svmSubIp=192.168.0.86
export svmCpu=3,4
export ensembleVolumes=/home/zjq/wym/code/fault/ensemble:/exp
export ensembleSubIp=192.168.0.190
export ensembleCpu=4,5
docker-compose -f ../../losso.yml up -d
docker-compose -f ../../knn.yml up -d
export decision=decision45
docker-compose -f ../../svm.yml up -d
export decision=decision45
export xgboostVolumes=/home/zjq/wym/code/fault/xgboost:/exp
export xgboostSubIp=192.168.0.190
export xgboostPubIp=192.168.0.53
export xgboostCpu=7,6
docker-compose -f ../../xgboost.yml up -d
