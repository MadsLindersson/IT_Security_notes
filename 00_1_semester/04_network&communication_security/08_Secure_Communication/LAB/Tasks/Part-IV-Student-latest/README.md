# MoSec Lab Part IV — HTTP, Nginx and TLS

This Part IV lab uses a reduced Part III security baseline. Unrelated rules from previous exercises have been omitted for simplicity so the focus remains on web communication and TLS.

## Requirements

- Rootful Docker Engine 28+ with Linux containers on AMD64 or ARM64; Docker Desktop is optional.
- Docker Compose V2 2.36.0+ (newer versions also supported), for `interface_name` and `gw_priority`. See the [Compose network reference](https://docs.docker.com/reference/compose-file/services/#interface_name).
- Make, Bash, curl, Python 3 and OpenSSL
- Wireshark is optional

## Start

From the repository root run this cmd (it uses the Makefile):

```bash
make start
```
or with docker compose:
```bash
docker compose up -d --build
```

No environment variables or manual directory preparation are needed. The starting state has an HTTP reverse proxy on Nginx TCP/80 and the Python portal on `0.0.0.0:8080`. Router policy permits Admin, Employee and host/WAN HTTP to Server, blocks direct backend access and HTTPS, and preserves Admin SSH and user/Server outbound Internet. TLS, certificates, HTTPS firewall permissions and optional HSTS remain student work.

| Service | URL | Credentials |
|---|---|---|
| Router GUI | http://localhost:8082/firewall | `admin / admin` |
| MoSec Ltd. Staff Portal through Nginx | http://localhost:8080/ | `alice / alice123` or `bob / bob123` |
| Nginx HTTP alias | http://localhost:80/ | Same portal accounts |

Host port 8080 reaches Nginx on Server port 80 through the relay and Router. Nginx forwards to `http://127.0.0.1:8080` inside Server; host port 8082 belongs to the Router GUI, whose internal port is also 8080. These ports are in separate network namespaces.

Portal accounts and employee data are fictional. HTTPS/443 is not serving TLS at startup.

Follow the [Part IV Student Guide](docs/PART_IV_STUDENT_GUIDE.md) to complete the exercise.

## Reset

```bash
make reset
```

Reset recreates the lab containers and discards container-local configuration, certificates and policy changes. Host files and manually installed host/browser CA trust are unchanged. Reload Nginx while working; restarting Server restores its HTTP baseline, removes Nginx certificates and container-local CA trust, and resets `/etc/mosec/portal-bind` to `0.0.0.0`. Use `supervisorctl restart portal` inside Server to apply a binding change without restarting the container. `make stop` also removes containers. Save work outside containers before stopping, starting or resetting the lab.

## Network and portability

Five separate Docker underlay bridges carry the teaching addresses below. Bootstrap `192.0.2.x` addresses are removed inside containers; Docker LAN masquerading is disabled. Only Router has WAN connectivity. The relay has only the management network, so portal traffic crosses Router filtering and DNAT/SNAT.

| Role | Address | Gateway | Router interface |
|---|---|---|---|
| Admin | 10.10.0.10/27 | 10.10.0.1 | eth1 |
| Employee | 10.10.0.42/27 | 10.10.0.33 | eth2 |
| Server | 10.10.0.74/27 | 10.10.0.65 | eth3 |
| Guest | 10.10.0.106/27 | 10.10.0.97 | eth4 |
| Printer | 10.10.0.138/27 | 10.10.0.129 | eth5 |

Router WAN is eth0 (`172.30.255.2/24`). Interface names are checked against attachment MACs before initialization. Images use native multi-architecture Debian/Python bases without an architecture override or host networking. On macOS/Windows, use a Linux Docker VM; Desktop is one option. Host URLs refer to the Docker host, so a remote Docker context needs forwarding to that host.

`make start` and `make reset` recreate container-local lab work. Both run platform checks first. Run Part III and IV separately because they share container names and project identity. No Part III controller, saved policy, credentials or runtime state is imported.

Run `./scripts/test-part4.sh` for the baseline suite (includes temporary listeners, removed automatically), or add `--read-only` to omit those probes. Checks cover separate LANs, addressing, NAT, HTTP-only filtering, SSH, Internet, GUI rule metadata, both portal accounts and sessions, and inactive TLS. These checks target the starting state, not a completed student TLS exercise.
