export svmVolumes=/home/nano/code/wafer/svm:/exp
export svmSubIp=192.168.0.53
export svmPubIp=192.168.0.190
export svmCpu=3
docker-compose -f ../svm.yml up -d
