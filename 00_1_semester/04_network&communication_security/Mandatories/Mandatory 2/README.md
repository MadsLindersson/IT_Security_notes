# MoSec Lab Part II

## Before switching from Lecture 5

Stop the Lecture 5 lab from its own directory with `make stop` (or its documented shutdown command) before starting Lecture 6. Both labs use the same Docker Compose project and container names.


This package contains the Part II ACL, firewall, spoofing, and anti-spoofing lab.

Start the lab:

```bash
docker compose up --build -d
```

Check containers:

```bash
docker compose ps
docker ps
```

Open the router GUI:

```text
http://localhost:8082

admin / admin
```

Read the exercise:

```text
docs/PART_II_STUDENT_GUIDE.md
```

Stop the lab:

```bash
docker compose down
```

Reset to the clean Part II starting state:

```bash
docker compose down
docker compose up --build -d
```

