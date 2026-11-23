FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/certificates \
    && chown -R appuser:appuser /app

USER appuser
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
