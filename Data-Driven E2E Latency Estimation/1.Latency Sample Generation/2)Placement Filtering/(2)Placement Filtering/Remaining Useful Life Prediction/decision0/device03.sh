export decision=decision0
39.100.79.76
export preprocessVolumes=/root/wym/code/rul/preprocess:/exp
export preprocessPubIp=39.100.79.76
export preprocessSubIp=39.100.79.76
export preprocessCpu=0
export predictVolumes=/root/wym/code/rul/predict:/exp
export predictSubIp=39.100.79.76
export predictCpu=3,2,1
docker-compose -f ../preprocess.yml up -d
docker-compose -f ../predict.yml up -d
export decision=decision0
