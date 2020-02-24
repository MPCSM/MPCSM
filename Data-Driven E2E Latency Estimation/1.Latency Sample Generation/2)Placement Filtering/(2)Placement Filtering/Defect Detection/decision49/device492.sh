export decision=decision49
192.168.0.190
192.168.0.86
export autoVolumes=/home/zjq/wym/code/wafer/auto:/exp
export autoPubIp=192.168.0.53
export autoSubIp=192.168.0.190
export autoCpu=3,4,5
export statisVolumes=/home/ljr/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.86
export statisCpu=9,10,11
export cnnVolumes=/home/nano/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.86
export cnnSubIp=192.168.0.53
export cnnCpu=0,1,2
export ensembleVolumes=/home/ljr/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=7,8
docker-compose -f ../auto.yml up -d
