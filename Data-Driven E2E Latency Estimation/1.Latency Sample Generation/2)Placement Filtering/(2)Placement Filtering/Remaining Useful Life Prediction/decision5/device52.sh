export decision=decision5
192.168.0.190
export preprocessVolumes=/home/zjq/wym/code/rul/preprocess:/exp
export preprocessPubIp=192.168.0.190
export preprocessSubIp=192.168.0.190
export preprocessCpu=0
export predictVolumes=/home/zjq/wym/code/rul/predict:/exp
export predictSubIp=192.168.0.190
export predictCpu=3,2,1
docker-compose -f ../preprocess.yml up -d
docker-compose -f ../predict.yml up -d
export decision=decision5
