FROM debian:12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      apt \
      bash \
      curl \
      ca-certificates \
      dnsutils \
      hping3 \
      iproute2 \
      iptables \
      iputils-ping \
      netcat-openbsd \
      openssl \
      openssh-server \
      python3 \
      nginx \
      supervisor \
      tcpdump \
      traceroute \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd \
    && useradd -m -s /bin/bash student \
    && echo "student:student" | chpasswd \
    && sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

COPY webapp.py portal_data.py /app/
COPY templates /app/templates
COPY static /app/static
RUN cp -a /etc/nginx /opt/nginx-baseline
COPY nginx /opt/part4
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY udp.sh /app/udp.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
