export decision=decision14
192.168.0.86
192.168.0.53
export autoVolumes=/home/ljr/code/wafer/auto:/exp
export autoPubIp=192.168.0.86
export autoSubIp=192.168.0.86
export autoCpu=9,10,11
export statisVolumes=/home/nano/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.53
export statisCpu=0,1,2
export cnnVolumes=/home/ljr/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.190
export cnnSubIp=192.168.0.86
export cnnCpu=6,7,8
export ensembleVolumes=/home/zjq/wym/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.190
export ensembleCpu=4,5
docker-compose -f ../ensemble.yml up -d