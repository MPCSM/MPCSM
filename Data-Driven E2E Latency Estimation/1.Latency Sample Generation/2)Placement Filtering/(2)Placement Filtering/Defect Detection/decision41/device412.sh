export decision=decision41
192.168.0.86
192.168.0.190
export autoVolumes=/home/ljr/code/wafer/auto:/exp
export autoPubIp=192.168.0.190
export autoSubIp=192.168.0.86
export autoCpu=9,10,11
export statisVolumes=/home/zjq/wym/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.190
export statisCpu=3,4,5
export cnnVolumes=/home/zjq/wym/code/wafer/cnn:/exp
export cnnPubIp=39.100.79.76
export cnnSubIp=192.168.0.190
export cnnCpu=0,1,2
export ensembleVolumes=/root/wym/code/wafer/ensemble:/exp
export ensembleSubIp=39.100.79.76
export ensembleCpu=14,15
docker-compose -f ../statis.yml up -d
docker-compose -f ../cnn.yml up -d
export decision=decision41