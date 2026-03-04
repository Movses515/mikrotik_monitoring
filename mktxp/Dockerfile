FROM python:3.11-slim

WORKDIR /home/mktxp

# Install mktxp from PyPI
RUN pip install --no-cache-dir mktxp

# Ensure config directory exists; config will be mounted at runtime
RUN mkdir -p /home/mktxp/mktxp

EXPOSE 49090

ENTRYPOINT ["mktxp"]

