# MoSec — Part IV: Student Guide

**Secure Web Communication | Network & Communication Security — Lecture 8**

## Lab overview

In this lab, you will investigate HTTP communication, Nginx reverse proxy behavior, backend exposure, firewall rules, TLS certificates and trusted HTTPS communication.

The environment continues from Part III with a simplified firewall policy. You will progressively secure the MoSec **Staff Portal** through observation, configuration, testing and troubleshooting.

### Resources

- [Cert-Helper.zip](https://ek.itslearning.com/ContentArea/ContentArea.aspx?LocationID=7920&LocationType=1&TextURL=%2fLearningToolElement%2fViewLearningToolElement.aspx%3fLearningToolElementId%3d1578174) — Certificate generation (beginner interface and advanced CLI option).
- [tls-weak-cipher-demo.py.zip](https://ek.itslearning.com/ContentArea/ContentArea.aspx?LocationID=7920&LocationType=1&TextURL=%2fLearningToolElement%2fViewLearningToolElement.aspx%3fLearningToolElementId%3d1577878) — Observe failed TLS negotiation.
- [crypto-visuals.zip](https://ek.itslearning.com/ContentArea/ContentArea.aspx?LocationID=7920&LocationType=1&TextURL=%2fLearningToolElement%2fViewLearningToolElement.aspx%3fLearningToolElementId%3d1578164) — Optional cryptography visualizations, also useful for Applied Cryptography.

Useful references: [Nginx](https://nginx.org/en/docs/), [Nginx HTTPS](https://nginx.org/en/docs/http/configuring_https_servers.html), [OpenSSL](https://docs.openssl.org/).

## Part 1 — Observe TLS with Wireshark

### Task 1.1 — Inspect a TLS handshake

1. Start Wireshark on your active network interface.
2. Open an incognito browser window and visit `https://ek.dk`.
3. Locate the TLS handshake and inspect ClientHello, ServerHello and available certificate information.
4. Use the browser certificate viewer or OpenSSL to inspect certificate details not visible in the capture.

*Note: TLS 1.3 encrypts most handshake messages after ServerHello.*

### Task 1.2 — Investigate failed TLS negotiation

Download and run `tls-weak-cipher-demo.py.zip` according to its instructions.

Capture the attempted connection in Wireshark and compare the failed negotiation with the successful handshake from Task 1.1.

## Part 2 — Explore the MoSec environment

### Task 2.1 — Start and inspect

Start the lab:

```bash
make start
docker compose ps
```

| Component | Address / service |
|---|---|
| Admin | See README address table |
| Employee | See README address table |
| Server | `10.10.0.74/27` |
| Server gateway | `10.10.0.65` |
| Python Staff Portal backend | TCP/8080 (inside Server) |
| Nginx | TCP/80 initially; TCP/443 later |
| Staff Portal via host | `http://localhost:8080` |
| Router/Firewall GUI | `http://localhost:8082/firewall` |

Host port 8080 reaches Nginx on Server port 80. Nginx proxies to `http://127.0.0.1:8080` inside Server. Host port 8082 is the Router GUI, not the Python backend.

Router GUI lab credentials: `admin / admin`.

Inspect the containers, network interfaces, listening services and Router ACL/firewall rules.

Useful commands:

```bash
docker exec <container> ip addr
docker exec <container> ss -lntp
docker exec <container> iptables -L <chain> -nv --line-numbers
```

### Task 2.2 — Test the Staff Portal

Access the Staff Portal through Nginx and log in using one of the fictional accounts:

- `alice / alice123`
- `bob / bob123`

Verify the dashboard and profile pages.

Investigate direct access to the Python backend using the Server IP address and backend port. Compare this with access through Nginx and from inside the Server container.

## Part 3 — Investigate and restrict backend exposure

### Task 3.1 — Discover the application binding

The Staff Portal consists of Nginx and a Python application running inside the Server container.

Inspect the Python application's listening address, running process and startup configuration.

Useful commands:

```bash
docker exec server ss -lntp
docker exec server ps aux
```

Locate the configuration controlling the application's listening address.

**Hint:** The Python application reads its listening configuration from a file under `/etc/mosec/`.

### Task 3.2 — Restrict direct access

Configure the Python application so that access through Nginx remains functional while direct access through the Server network interface is restricted.

1. Locate and modify the application binding configuration.
2. Identify how the Python application is started.
3. Restart the Python application to apply the change.
4. Verify the new listening address.

**Hint:** The Python application reads its binding configuration when it starts. Reloading Nginx does not apply changes to Python.

Avoid restarting the entire Server container without verifying whether its configuration changes will persist.

### Task 3.3 — Verify the result

Retest:

- Client → Nginx → Python
- Client → Python directly

Verify that the Staff Portal remains accessible through Nginx and that direct backend access is restricted.

Review the Router firewall policy as an additional security control.

## Part 4 — Observe insecure HTTP communication

### Task 4.1 — Capture HTTP traffic

Start a packet capture on the Router interface facing the Server or another suitable observation point.

Generic command:

```bash
tcpdump -ni <interface> -s0 -A "tcp port <port>"
```

Generate HTTP traffic by logging into the Staff Portal using fictional credentials.

Inspect the HTTP requests and readable application data. Keep your observations for the later HTTPS comparison.

## Part 5 — Generate the certificate hierarchy

### Task 5.1 — Create certificates

Use `Cert-Helper.zip` to generate the following certificate hierarchy:

**Root CA → Intermediate CA → Server certificate**

The Server certificate must contain `DNS:mosec.test` in its Subject Alternative Name (SAN).

Use the beginner interface or the optional advanced command-line approach.

### Task 5.2 — Prepare certificates for Nginx

Export the necessary public certificates and the Server private key.

Prepare the certificate chain and place the required files in the appropriate Nginx directories.

Keep CA private keys outside the Server container.

Consult the [Nginx HTTPS documentation](https://nginx.org/en/docs/http/configuring_https_servers.html).

## Part 6 — Configure HTTPS in Nginx

### Task 6.1 — Configure TLS termination

Inspect the existing Nginx configuration:

```bash
docker exec <container> cat <nginx-config-path>
```

Configure Nginx to accept HTTPS connections using the Server certificate and private key.

Preserve the reverse proxy connection to the local Python backend.

Validate and reload the Nginx configuration:

```bash
nginx -t
nginx -s reload
```

Run these commands inside the appropriate container.

### Task 6.2 — Investigate HTTPS connectivity

Attempt to access the Staff Portal over HTTPS from the host and authorized client containers.

Use a browser, curl or another suitable tool.

If the connection fails, investigate:

- The Nginx listening ports and service status.
- Container network connectivity.
- Router firewall rules and effective rule order.
- Firewall counters and connection behavior.

Resolve the connectivity issue before proceeding.

Keep HTTP available temporarily for comparison.

## Part 7 — Configure hostname resolution and certificate trust

### Task 7.1 — Configure the `mosec.test` hostname

The lab uses `mosec.test` as the Staff Portal hostname. This is a local testing domain and is not configured in public DNS.

To access the portal using this hostname, add a local entry to the hosts file on the machine running your browser.

**On macOS or Kali/Linux:**

Open a terminal and edit the hosts file:

```bash
sudo nano /etc/hosts
```

Add an entry mapping the hostname to the appropriate address:

```text
<IP_ADDRESS> mosec.test
```

Choose the IP address based on where your browser runs:

| Browser location | Address to use |
|---|---|
| Host computer using Docker's published HTTPS port | `127.0.0.1` |
| Kali/Ubuntu VM with direct network access to the Server | The Server's reachable IP address |
| Client container | The Server IP address, if reachable through the configured network policy |

For example, if you access HTTPS through the host's Docker forwarding:

```text
127.0.0.1 mosec.test
```

Save the file in Nano using `Ctrl + O`, Enter, then `Ctrl + X`.

Verify hostname resolution:

```bash
getent hosts mosec.test    # Linux
dscacheutil -q host -a name mosec.test    # macOS
```

You can also use `curl` to test the connection.

**Note:** Each VM or container has its own hostname resolution configuration. Editing `/etc/hosts` on your Mac does not automatically update `/etc/hosts` inside Kali or Docker containers.

### Task 7.2 — Inspect the browser warning

Open:

`https://mosec.test`

Before importing certificates, inspect the browser's certificate warning and connection-security information.

Do not bypass the warning as the solution.

### Task 7.3 — Establish trust

Use the appropriate operating-system or browser trust-store mechanism to trust the **public Root CA certificate** generated for this lab.

Reconnect and verify the trusted HTTPS connection, certificate chain, hostname and Staff Portal functionality.

Depending on the browser, connection-security information may appear through a lock icon or another site-information control.

Never install or distribute CA private keys.

## Part 8 — Compare HTTP and HTTPS

### Task 8.1 — Capture TLS communication

Repeat the earlier packet capture using HTTPS.

Generic command:

```bash
tcpdump -ni <interface> -s0 -X "tcp port <port>"
```

Alternatively, use Wireshark.

Generate traffic by logging into the Staff Portal.

Compare the observable HTTP and HTTPS communication, including handshake information, negotiated TLS parameters and application-data visibility.

Use OpenSSL or browser certificate information to supplement your capture.

### Task 8.2 — Investigate TLS termination

Optionally, capture traffic between Nginx and Python using the Server container's loopback interface.

Compare the local backend communication with the encrypted client connection.

## Part 9 — Enforce HTTPS-only access

### Task 9.1 — Review the security policy

MoSec requires authorized users to access the Staff Portal through HTTPS only.

Review and adjust the Router firewall policy while preserving necessary administrative and Internet connectivity.

Review the Nginx HTTP listener and determine whether it remains necessary.

### Task 9.2 — Verify the final configuration

Test from the Host, Admin and Employee environments.

Verify that:

- Trusted HTTPS access works.
- Plaintext HTTP access from client networks is restricted.
- Direct Python backend access is prevented.
- Required SSH and Internet connectivity remain functional.
- Login, dashboard and profile work through Nginx.

## Optional — HSTS and cryptography visualization

If time permits, investigate HTTP Strict Transport Security (HSTS) and its role in browser HTTPS enforcement.

See the [MDN HSTS documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security).

You may also explore `crypto-visuals.zip` for additional cryptographic visualizations relevant to this lab and Applied Cryptography.

## Reset and cleanup

Both `make start` and `make reset` recreate containers and discard all container-local work. `make stop` removes containers too. There are no persistent volumes for student changes. Save configuration and certificates outside containers before using these commands.

Even restarting the existing Server container restores Nginx to HTTP-only, removes certificates under `/etc/nginx`, clears container-local CA trust, and resets `/etc/mosec/portal-bind` to `0.0.0.0`. Reload Nginx to apply Nginx changes; use `supervisorctl restart portal` inside Server to apply Python binding changes. Restarting Router restores its baseline firewall policy.

Use `make reset` to restore the unsolved baseline. The validation scripts check this baseline and are not expected to pass after completing the TLS or backend-hardening exercises.

Locally saved files and certificates installed in the host's trust store may remain after a Docker reset. Remove temporary lab trust when finished.

Remove the temporary `mosec.test` entry from `/etc/hosts` when you no longer need the lab configuration.

**No submission is required for this lab.**