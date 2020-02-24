export decision=decision40
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
export ensembleCpu=1,2
docker-compose -f ../../svm.yml up -d
