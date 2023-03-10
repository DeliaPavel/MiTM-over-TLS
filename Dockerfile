FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
        iputils-ping net-tools iproute2 bash openssl wget unzip bsdmainutils ssh vim dsniff sslstrip iptables curl tcpdump

COPY start.sh .
CMD ./start.sh