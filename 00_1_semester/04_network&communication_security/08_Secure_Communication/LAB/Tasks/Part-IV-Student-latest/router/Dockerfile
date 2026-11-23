FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      apt \
      bash \
      curl \
      dnsutils \
      iproute2 \
      iptables \
      iputils-ping \
      iputils-arping \
      netcat-openbsd \
      procps \
      tcpdump \
      traceroute \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/init-part2.sh

EXPOSE 8080
ENTRYPOINT ["/app/entrypoint.sh"]
