# ./dnsmasq/Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y dnsmasq
COPY dnsmasq.conf /etc/dnsmasq.conf
CMD ["dnsmasq", "-k"]