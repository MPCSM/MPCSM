export decision=decision48
192.168.0.190
192.168.0.53
export autoVolumes=/home/zjq/wym/code/wafer/auto:/exp
export autoPubIp=39.100.79.76
export autoSubIp=192.168.0.190
export autoCpu=3,4,5
export statisVolumes=/home/nano/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.53
export statisCpu=0,1,2
export cnnVolumes=/root/wym/code/wafer/cnn:/exp
export cnnPubIp=39.100.79.76
export cnnSubIp=39.100.79.76
export cnnCpu=13,14,15
export ensembleVolumes=/root/wym/code/wafer/ensemble:/exp
export ensembleSubIp=39.100.79.76
export ensembleCpu=11,12
docker-compose -f ../auto.yml up -d