FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    net-tools \
    tcpdump \
    dsniff \
    iproute2 \
    iputils-ping \
    git \
    curl \
    wget \
    build-essential \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala Scapy via pip (última versão)
RUN pip install --no-cache-dir scapy

WORKDIR /app

# Copiar todos os scripts MITM
COPY *.py ./

CMD ["python", "arp_spoof.py"]
