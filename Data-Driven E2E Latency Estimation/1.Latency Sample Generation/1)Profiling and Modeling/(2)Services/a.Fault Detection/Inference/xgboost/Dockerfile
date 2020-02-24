FROM ubuntu:bionic
ADD sources.list /etc/apt/sources.list
RUN apt update && \
  apt install python3 net-tools iputils-ping python3-pip mosquitto nano -y  && \
  pip3 install paho-mqtt pandas -i https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip3 install sklearn xgboost -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN mkdir /exp

WORKDIR /exp
