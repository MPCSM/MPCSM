export decision=decision1
192.168.0.53
export preprocessVolumes=/home/nano/code/rul/preprocess:/exp
export preprocessPubIp=192.168.0.190
export preprocessSubIp=192.168.0.53
export preprocessCpu=0
export predictVolumes=/home/zjq/wym/code/rul/predict:/exp
export predictSubIp=192.168.0.190
export predictCpu=2,1,0
docker-compose -f ../predict.yml up -d
