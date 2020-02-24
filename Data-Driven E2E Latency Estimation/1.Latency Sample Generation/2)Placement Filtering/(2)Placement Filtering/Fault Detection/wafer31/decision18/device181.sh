export decision=decision18
192.168.0.190
export lossoVolumes=/home/zjq/wym/code/fault/losso:/exp
export lossoPubIp1=192.168.0.86
export lossoPubIp2=192.168.0.190
export lossoPubIp3=192.168.0.190
export lossoSubIp=192.168.0.190
export lossoCpu=2,3
export knnVolumes=/home/ljr/code/fault/knn:/exp
export knnPubIp=192.168.0.86
export knnSubIp=192.168.0.86
export knnCpu=4,5
export svmVolumes=/home/zjq/wym/code/fault/svm:/exp
export svmPubIp=192.168.0.86
export svmSubIp=192.168.0.190
export svmCpu=0,1
export ensembleVolumes=/home/ljr/code/fault/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=2,3
docker-compose -f ../../losso.yml up -d
docker-compose -f ../../knn.yml up -d
export decision=decision18
