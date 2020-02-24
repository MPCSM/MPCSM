FROM pytorch/pytorch:1.0-cuda10.0-cudnn7-runtime
ADD sources.list /etc/apt/sources.list
RUN apt update && \
  apt install net-tools iputils-ping  mosquitto nano -y  && \
  pip install paho-mqtt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip install Pillow bitarray -i https://pypi.tuna.tsinghua.edu.cn/simple && \
  rm -rf /var/lib/apt/lists/* && rm -rf ~/.cache/pip
RUN mkdir /exp

WORKDIR /exp
