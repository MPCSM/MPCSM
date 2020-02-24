FROM ubuntu:bionic
ADD sources.list /etc/apt/sources.list
RUN apt update && \
  apt install python3 net-tools iputils-ping python3-pip mosquitto nano -y  && \
  pip3 install paho-mqtt pandas schedule -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN mkdir /exp
CMD "mosquitto -c /etc/mosquitto/mosquitto.conf -d"
WORKDIR /exp
