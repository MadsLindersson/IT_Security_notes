FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends apt \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY proxy.py .
EXPOSE 8080
CMD ["python", "/app/proxy.py"]
