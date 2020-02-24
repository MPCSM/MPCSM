export decision=decision0
192.168.0.53
export preprocessVolumes=/home/nano/code/rul/preprocess:/exp
export preprocessPubIp=39.100.79.76
export preprocessSubIp=192.168.0.53
export preprocessCpu=0
export predictVolumes=/root/wym/code/rul/predict:/exp
export predictSubIp=39.100.79.76
export predictCpu=2,1,0
docker-compose -f ../predict.yml up -d
