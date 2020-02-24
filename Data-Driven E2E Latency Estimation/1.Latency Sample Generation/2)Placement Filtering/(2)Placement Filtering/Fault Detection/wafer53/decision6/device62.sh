export decision=decision6
192.168.0.190
export lossoVolumes=/home/zjq/wym/code/fault/losso:/exp
export lossoPubIp1=192.168.0.86
export lossoPubIp2=192.168.0.190
export lossoPubIp3=192.168.0.190
export lossoSubIp=192.168.0.190
export lossoCpu=4,5
export knnVolumes=/home/ljr/code/fault/knn:/exp
export knnPubIp=192.168.0.190
export knnSubIp=192.168.0.86
export knnCpu=2,3
export svmVolumes=/home/zjq/wym/code/fault/svm:/exp
export svmPubIp=192.168.0.190
export svmSubIp=192.168.0.190
export svmCpu=2,3
export ensembleVolumes=/home/zjq/wym/code/fault/ensemble:/exp
export ensembleSubIp=192.168.0.190
export ensembleCpu=0,1
docker-compose -f ../../svm.yml up -d
export xgboostVolumes=/home/zjq/wym/code/fault/xgboost:/exp
export xgboostSubIp=192.168.0.190
export xgboostPubIp=192.168.0.53
export xgboostCpu=7,6
docker-compose -f ../../xgboost.yml up -d
