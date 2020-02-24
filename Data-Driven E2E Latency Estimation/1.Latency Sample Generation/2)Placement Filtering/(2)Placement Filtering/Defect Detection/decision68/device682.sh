export decision=decision68
39.100.79.76
192.168.0.190
export autoVolumes=/root/wym/code/wafer/auto:/exp
export autoPubIp=39.100.79.76
export autoSubIp=39.100.79.76
export autoCpu=13,14,15
export statisVolumes=/home/zjq/wym/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.190
export statisCpu=3,4,5
export cnnVolumes=/root/wym/code/wafer/cnn:/exp
export cnnPubIp=39.100.79.76
export cnnSubIp=39.100.79.76
export cnnCpu=10,11,12
export ensembleVolumes=/root/wym/code/wafer/ensemble:/exp
export ensembleSubIp=39.100.79.76
export ensembleCpu=8,9
docker-compose -f ../statis.yml up -d
