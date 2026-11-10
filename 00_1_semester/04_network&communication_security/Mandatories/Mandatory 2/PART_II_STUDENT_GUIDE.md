# MoSec Lab Part II - IP ACLs, Spoofing, and Anti-Spoofing

Part II starts with routing already working.

Your task is to create and test security rules.

---

## 1. Verify Connectivity

Start Part II:

```bash
docker compose up --build -d
```

Check that the containers are running:

```bash
docker compose ps
docker ps
```

Stop the lab:

```bash
docker compose down
```

Reset the lab to the clean Part II starting state:

```bash
docker compose down
docker compose up --build -d
```

Open the router GUI:

```text
http://localhost:8082

admin / admin
```

Inspect Docker networks:

```bash
docker network ls

docker network inspect mosec-router-lab_admin_net
docker network inspect mosec-router-lab_server_net
docker network inspect mosec-router-lab_guest_net
docker network inspect mosec-router-lab_printer_net

```

Inspect addressing and routes:

```bash
docker exec admin ip -br addr
docker exec admin ip route

docker exec employee ip -br addr
docker exec employee ip route

docker exec server ip -br addr
docker exec server ip route

docker exec guest ip -br addr
docker exec guest ip route

docker exec printer ip -br addr
docker exec printer ip route
```

Record:

| Host     | IPv4/CIDR | Default Gateway | Local Network |
| -------- | --------- | --------------- | ------------- |
| Admin    |           |                 |               |
| Employee |           |                 |               |
| Server   |           |                 |               |
| Guest    |           |                 |               |
| Printer  |           |                 |               |

Test connectivity:

```bash
docker exec admin ping -c 2 [IP_ADDR]
```

Record:

| Test                 | Result |
| -------------------- | ------ |
| Admin -> Employee    |        |
| Admin -> Server      |        |
| Admin -> Printer     |        |
| Admin -> Guest       |        |
| Admin -> Internet    |        |
| Employee -> Admin    |        |
| Employee -> Server   |        |
| Employee -> Printer  |        |
| Employee -> Guest    |        |
| Employee -> Internet |        |
| Guest -> Admin       |        |
| Guest -> Employee    |        |
| Guest -> Server      |        |
| Guest -> Printer     |        |
| Guest -> Internet    |        |

Reflect:

Is the current Guest access appropriate for a Guest network?

---

## 2. Security Requirement

The company wants this policy:

| Traffic              | Action |
| -------------------- | ------ |
| Admin -> Employee    | ALLOW  |
| Admin -> Server      | ALLOW  |
| Admin -> Printer     | ALLOW  |
| Admin -> Internet    | ALLOW  |
| Employee -> Admin    | ALLOW  |
| Employee -> Server   | ALLOW  |
| Employee -> Printer  | ALLOW  |
| Employee -> Internet | ALLOW  |
| Guest -> Admin LAN   | DENY   |
| Guest -> Server LAN  | DENY   |
| Guest -> Printer LAN | DENY   |
| Guest -> Internet    | ALLOW  |

Use the ACL section of the router GUI to implement the policy.

Generic ACL syntax:

```text
Source: Admin host
Destination: Server network
Action: ALLOW
Description: admin to server
```

```text
Source: Guest network
Destination: Printer network
Action: DENY
Description: guest to printer
```

Determine the actual IPv4/CIDR values from your inspection results.

---

## 3. Test The ACL

Run:

```bash
docker exec admin ping -c 2 [IP_ADDR]
```

Record:

| Test | Result |
| --- | --- |
| Admin -> Server | |
| Admin -> Printer | |
| Admin -> Internet | |
| Employee -> Server | |
| Employee -> Printer | |
| Employee -> Internet | |
| Guest -> Admin | |
| Guest -> Employee | |
| Guest -> Server | |
| Guest -> Printer | |
| Guest -> Internet | |

Reflect:

Does the implemented policy behave as required?

---

## 4. Spoofing Test

Monitor Server:

```bash
docker exec server tcpdump -ni any 'icmp'
```

Monitor Admin in another terminal:

```bash
docker exec admin tcpdump -ni any 'icmp'
```

Send one controlled spoofed packet from Guest:

```bash
docker exec guest hping3 --icmp -c 1 -a [FORGED_IP] [TARGET_IP]
```

Repeat the packet if needed while tcpdump is running.

Reflect:

1. What source IP does Server observe?
2. Does Admin observe ICMP traffic?
3. Is the source IP alone enough to identify where the packet really came from?

---

## 5. First Anti-Spoofing Rule

Source addresses can be checked against the interface where the packet entered the router.

Use the Firewall section of the GUI to create an ingress anti-spoofing rule.

Generic firewall syntax:

```text
Incoming Zone: Guest LAN
Source: Admin LAN
Destination: Any
Action: DENY
Description: guest anti-spoof
```

Determine the actual IPv4/CIDR value from your inspection results.

Repeat the same spoofing test:

```bash
docker exec server tcpdump -ni any 'icmp'
```

```bash
docker exec admin tcpdump -ni any 'icmp'
```

```bash
docker exec guest hping3 --icmp -c 1 -a [FORGED_IP] [TARGET_IP]
```

Record the result.

---

## 6. Rule Order Teaching Moment

If the spoofed packet still reaches Server, inspect the Effective Rule Order in the router GUI.

Reflect:

Why might a correct DENY rule still not take effect?

Do:

1. Inspect the effective rule order.
2. Change the priority if you think it is necessary.
3. Repeat the exact same spoofing test.
4. Compare the tcpdump results.

---

## 7. Test Other Spoofed Sources

Spoof Server:

```bash
docker exec guest hping3 --icmp -c 1 -a [FORGED_IP] [TARGET_IP]
```

Spoof Printer:

```bash
docker exec guest hping3 --icmp -c 1 -a [FORGED_IP] [TARGET_IP]
```

Use the previous anti-spoofing example to create any additional rules you think are required.

Generic examples:

```text
Incoming Guest LAN + source Server LAN -> DENY
```

```text
Incoming Guest LAN + source Printer LAN -> DENY
```

Determine the actual IPv4/CIDR values yourself.

---

## 8. Final Verification

Run:

```bash
docker exec guest hping3 --icmp -c 1 -a [FORGED_IP] [TARGET_IP]
```

Test legitimate Guest Internet access:

```bash
docker exec guest ping -c 2 1.1.1.1
```

Record:

| Test | Result |
| --- | --- |
| Guest spoofing Admin | |
| Guest spoofing Server | |
| Guest spoofing Printer | |
| Guest using real address -> Internet | |



