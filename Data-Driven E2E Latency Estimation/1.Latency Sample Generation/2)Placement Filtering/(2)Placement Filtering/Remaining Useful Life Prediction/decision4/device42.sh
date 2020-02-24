export decision=decision4
192.168.0.190
export preprocessVolumes=/home/zjq/wym/code/rul/preprocess:/exp
export preprocessPubIp=192.168.0.86
export preprocessSubIp=192.168.0.190
export preprocessCpu=0
export predictVolumes=/home/ljr/code/rul/predict:/exp
export predictSubIp=192.168.0.86
export predictCpu=2,1,0
docker-compose -f ../preprocess.yml up -d
