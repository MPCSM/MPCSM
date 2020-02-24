export decision=decision32
192.168.0.190
export lossoVolumes=/home/zjq/wym/code/fault/losso:/exp
export lossoPubIp1=192.168.0.190
export lossoPubIp2=192.168.0.86
export lossoPubIp3=192.168.0.190
export lossoSubIp=192.168.0.190
export lossoCpu=4,5
export knnVolumes=/home/zjq/wym/code/fault/knn:/exp
export knnPubIp=192.168.0.190
export knnSubIp=192.168.0.190
export knnCpu=2,3
export svmVolumes=/home/ljr/code/fault/svm:/exp
export svmPubIp=192.168.0.190
export svmSubIp=192.168.0.86
export svmCpu=4,5
export ensembleVolumes=/home/zjq/wym/code/fault/ensemble:/exp
export ensembleSubIp=192.168.0.190
export ensembleCpu=0,1
docker-compose -f ../../knn.yml up -d
