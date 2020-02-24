export decision=decision11
192.168.0.53
192.168.0.190
export autoVolumes=/home/nano/code/wafer/auto:/exp
export autoPubIp=192.168.0.190
export autoSubIp=192.168.0.53
export autoCpu=0,1,2
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
docker-compose -f ../ensemble.yml up -d
