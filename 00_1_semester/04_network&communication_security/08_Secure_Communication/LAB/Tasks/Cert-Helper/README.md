# Certificate Generation Lab

An educational lab for creating and inspecting a Certificate Authority (CA), a Certificate Signing Request (CSR), and server certificates. Use it to learn how keys, signing, and trust fit together. Certificates created here are for classroom practice, not production use.

## What will you learn?

- The difference between private and public keys.
- How a CSR requests a certificate.
- How a CA signs certificates.
- Why creating or signing a certificate does not automatically make it trusted.
- How to explore beginner and advanced certificate workflows.

## Requirements

- Docker with Docker Compose.
- A modern web browser.

## How to run

From the project directory, create your local configuration and start the lab:

```bash
cp .env.example .env
docker compose up --build
```

Open [http://localhost:9090](http://localhost:9090). To change the port, update `APP_PORT` in `.env`; Flask and Docker Compose use the same value.

Generated files are stored in `./certificates/`. Keep private-key files secret and remove any lab CA you import into a device after the exercise.

## Beginner and Advanced modes

Beginner Mode guides you through CA creation, trust concepts, CSR creation, signing, and inspection. Advanced Mode provides OpenSSL examples for the same lab concepts. Use the Inspector to review generated public certificate and CSR details.

## How to stop

```bash
docker compose down
```

## Run locally for development

Set `CERT_BASE_DIR=./certificates` in `.env`, then run:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Author

Institution: EK – Erhvervsakademi København  
Developed by: [moms@ek.dk](mailto:moms@ek.dk)
