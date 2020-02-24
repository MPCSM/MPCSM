FROM ubuntu:bionic
ADD sources.list /etc/apt/sources.list

RUN apt update && \
  apt install python3 python3-pip net-tools iputils-ping mosquitto nano -y  && \
  pip3 install paho-mqtt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip3 install pandas==0.22.0 sklearn scikit-image -i https://pypi.tuna.tsinghua.edu.cn/simple && \
  rm -rf /var/lib/apt/lists/* && rm -rf ~/.cache/pip
  
RUN mkdir /exp

WORKDIR /exp
