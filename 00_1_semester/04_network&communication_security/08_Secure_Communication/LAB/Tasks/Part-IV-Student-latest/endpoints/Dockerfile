FROM debian:12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      apt \
      bash \
      curl \
      dnsutils \
      hping3 \
      iproute2 \
      iputils-ping \
      netcat-openbsd \
      openssh-client \
      openssl \
      ca-certificates \
      tcpdump \
      traceroute \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
