export decision=decision1
192.168.0.86
export preprocessVolumes=/home/ljr/code/rul/preprocess:/exp
export preprocessPubIp=39.100.79.76
export preprocessSubIp=192.168.0.86
export preprocessCpu=0
export predictVolumes=/root/wym/code/rul/predict:/exp
export predictSubIp=39.100.79.76
export predictCpu=2,1,0
docker-compose -f ../predict.yml up -d
