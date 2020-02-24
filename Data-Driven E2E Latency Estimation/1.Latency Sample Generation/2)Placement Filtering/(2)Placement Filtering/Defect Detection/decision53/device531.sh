export decision=decision53
192.168.0.190
192.168.0.86
export autoVolumes=/home/zjq/wym/code/wafer/auto:/exp
export autoPubIp=192.168.0.86
export autoSubIp=192.168.0.190
export autoCpu=3,4,5
export statisVolumes=/home/ljr/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.86
export statisCpu=9,10,11
export cnnVolumes=/home/ljr/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.86
export cnnSubIp=192.168.0.86
export cnnCpu=6,7,8
export ensembleVolumes=/home/ljr/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=4,5
docker-compose -f ../statis.yml up -d
docker-compose -f ../cnn.yml up -d
export decision=decision53
docker-compose -f ../ensemble.yml up -d
export decision=decision53
