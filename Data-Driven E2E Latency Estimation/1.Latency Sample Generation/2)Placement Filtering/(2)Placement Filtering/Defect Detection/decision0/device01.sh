export decision=decision0
192.168.0.53
192.168.0.86
export autoVolumes=/home/nano/code/wafer/auto:/exp
export autoPubIp=192.168.0.86
export autoSubIp=192.168.0.53
export autoCpu=0,1,2
export statisVolumes=/home/ljr/code/wafer/statis:/exp
export statisPubIp=192.168.0.53
export statisSubIp=192.168.0.86
export statisCpu=9,10,11
export cnnVolumes=/home/ljr/code/wafer/cnn:/exp
export cnnPubIp=192.168.0.86
export cnnSubIp=192.168.0.86
export cnnCpu=6,7,8
export ensembleVolumes=/home/ljr/code/wafer/ensemble:/exp
export ensembleSubIp=192.168.0.86
export ensembleCpu=4,5
docker-compose -f ../statis.yml up -d
docker-compose -f ../cnn.yml up -d
export decision=decision0
docker-compose -f ../ensemble.yml up -d
export decision=decision0
