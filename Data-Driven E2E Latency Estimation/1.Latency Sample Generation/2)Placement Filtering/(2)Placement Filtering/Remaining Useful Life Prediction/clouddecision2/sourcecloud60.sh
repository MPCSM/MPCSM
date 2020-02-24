export number=cloud60
export sourceSubIp=192.168.0.190
docker-compose -f ../end.yml up -d
docker-compose -f ../source.yml up -d
