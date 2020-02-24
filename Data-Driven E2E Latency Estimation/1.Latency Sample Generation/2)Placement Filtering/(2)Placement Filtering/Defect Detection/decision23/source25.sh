export number=25
export sourceSubIp1=192.168.0.86
export sourceSubIp2=192.168.0.86
docker-compose -f ../end.yml up -d
docker-compose -f ../source.yml up -d
