export decision=decision2
192.168.0.86
export preprocessVolumes=/home/ljr/code/rul/preprocess:/exp
export preprocessPubIp=192.168.0.86
export preprocessSubIp=192.168.0.86
export preprocessCpu=0
export predictVolumes=/home/ljr/code/rul/predict:/exp
export predictSubIp=192.168.0.86
export predictCpu=3,2,1
docker-compose -f ../preprocess.yml up -d
docker-compose -f ../predict.yml up -d
export decision=decision2
