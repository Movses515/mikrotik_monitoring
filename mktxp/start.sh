#!/bin/sh
# Start mktxp on internal port 49091
MKTXP_PORT=49091 mktxp --cfg-dir /etc/mktxp export &

# Wait for mktxp to start
sleep 3

# Start encoding proxy on port 49090 (what Prometheus scrapes)
exec python3 /opt/encoding_proxy.py
