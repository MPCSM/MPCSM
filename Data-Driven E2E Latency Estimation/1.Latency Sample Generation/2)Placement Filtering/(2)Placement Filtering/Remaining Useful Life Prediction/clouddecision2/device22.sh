export decision=decision2
192.168.0.190
export preprocessVolumes=/home/zjq/wym/code/rul/preprocess:/exp
export preprocessPubIp=39.100.79.76
export preprocessSubIp=192.168.0.190
export preprocessCpu=0
export predictVolumes=/root/wym/code/rul/predict:/exp
export predictSubIp=39.100.79.76
export predictCpu=2,1,0
docker-compose -f ../preprocess.yml up -d
