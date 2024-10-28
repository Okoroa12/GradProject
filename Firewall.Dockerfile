# ./firewall/Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y iptables
COPY rules.sh /rules.sh
RUN chmod +x /rules.sh
CMD ["/rules.sh"]