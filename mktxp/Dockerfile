FROM ghcr.io/akpw/mktxp:latest

COPY encoding_proxy.py /opt/encoding_proxy.py
COPY start.sh /opt/start.sh
RUN chmod +x /opt/start.sh

EXPOSE 49090

ENTRYPOINT ["/opt/start.sh"]
