export decision=decision32
192.168.0.86
192.168.0.190
export autoVolumes=/home/ljr/code/wafer/auto:/exp
export autoPubIp=192.168.0.53
export autoSubIp=192.168.0.86
export autoCpu=9,10,11
export statisVolumes=/home/zjq/wym/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.190
export statisCpu=3,4,5
export cnnVolumes=/home/nano/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.86
export cnnSubIp=192.168.0.53
export cnnCpu=0,1,2
export ensembleVolumes=/home/ljr/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=7,8
docker-compose -f ../auto.yml up -d
docker-compose -f ../ensemble.yml up -d
export decision=decision32
