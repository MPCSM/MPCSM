export decision=decision4
192.168.0.53
192.168.0.86
export autoVolumes=/home/nano/code/wafer/auto:/exp
export autoPubIp=192.168.0.190
export autoSubIp=192.168.0.53
export autoCpu=0,1,2
export statisVolumes=/home/ljr/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.86
export statisCpu=9,10,11
export cnnVolumes=/home/zjq/wym/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.190
export cnnSubIp=192.168.0.190
export cnnCpu=3,4,5
export ensembleVolumes=/home/zjq/wym/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.190
export ensembleCpu=1,2
docker-compose -f ../cnn.yml up -d
docker-compose -f ../ensemble.yml up -d
export decision=decision4
