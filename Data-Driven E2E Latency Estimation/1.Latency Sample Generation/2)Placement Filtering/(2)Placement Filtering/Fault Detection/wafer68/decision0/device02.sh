export xgboostVolumes=/home/zjq/wym/code/fault/xgboost:/exp
export xgboostSubIp=192.168.0.190
export xgboostPubIp=192.168.0.86
export xgboostCpu=7,6
docker-compose -f ../../xgboost.yml up -d
