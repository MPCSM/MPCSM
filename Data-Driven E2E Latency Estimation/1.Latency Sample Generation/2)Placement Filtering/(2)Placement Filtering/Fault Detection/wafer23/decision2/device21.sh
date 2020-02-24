export decision=decision2
192.168.0.86
export lossoVolumes=/home/ljr/code/fault/losso:/exp
export lossoPubIp1=192.168.0.190
export lossoPubIp2=192.168.0.190
export lossoPubIp3=192.168.0.190
export lossoSubIp=192.168.0.86
export lossoCpu=2,3
export knnVolumes=/home/zjq/wym/code/fault/knn:/exp
export knnPubIp=192.168.0.86
export knnSubIp=192.168.0.190
export knnCpu=4,5
export svmVolumes=/home/zjq/wym/code/fault/svm:/exp
export svmPubIp=192.168.0.86
export svmSubIp=192.168.0.190
export svmCpu=2,3
export ensembleVolumes=/home/ljr/code/fault/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=0,1
docker-compose -f ../../svm.yml up -d
