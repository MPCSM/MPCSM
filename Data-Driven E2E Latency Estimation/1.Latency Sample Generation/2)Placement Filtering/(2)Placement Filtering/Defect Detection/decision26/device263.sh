export decision=decision26
192.168.0.86
192.168.0.86
export autoVolumes=/home/ljr/code/wafer/auto:/exp
export autoPubIp=192.168.0.86
export autoSubIp=192.168.0.86
export autoCpu=9,10,11
export statisVolumes=/home/ljr/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.86
export statisCpu=6,7,8
export cnnVolumes=/home/ljr/code/wafer/cnn:/exp
export cnnPubIp=39.100.79.76
export cnnSubIp=192.168.0.86
export cnnCpu=3,4,5
export ensembleVolumes=/root/wym/code/wafer/ensemble:/exp
export ensembleSubIp=39.100.79.76
export ensembleCpu=14,15
docker-compose -f ../ensemble.yml up -d
