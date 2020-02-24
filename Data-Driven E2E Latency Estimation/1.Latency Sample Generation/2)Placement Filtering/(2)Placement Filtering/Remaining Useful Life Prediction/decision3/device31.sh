export decision=decision3
192.168.0.86
export preprocessVolumes=/home/ljr/code/rul/preprocess:/exp
export preprocessPubIp=192.168.0.190
export preprocessSubIp=192.168.0.86
export preprocessCpu=0
export predictVolumes=/home/zjq/wym/code/rul/predict:/exp
export predictSubIp=192.168.0.190
export predictCpu=2,1,0
docker-compose -f ../preprocess.yml up -d
