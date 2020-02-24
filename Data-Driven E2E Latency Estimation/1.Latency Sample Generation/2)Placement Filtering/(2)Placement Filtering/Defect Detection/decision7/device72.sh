export decision=decision7
192.168.0.53
192.168.0.190
export autoVolumes=/home/nano/code/wafer/auto:/exp
export autoPubIp=192.168.0.86
export autoSubIp=192.168.0.53
export autoCpu=0,1,2
export statisVolumes=/home/zjq/wym/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.190
export statisCpu=3,4,5
export cnnVolumes=/home/ljr/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.86
export cnnSubIp=192.168.0.86
export cnnCpu=9,10,11
export ensembleVolumes=/home/ljr/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=7,8
docker-compose -f ../statis.yml up -d
