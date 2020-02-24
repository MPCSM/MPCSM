export number=cloud60
export sourceSubIp=39.100.79.76
docker-compose -f ../end.yml up -d
docker-compose -f ../source.yml up -d
