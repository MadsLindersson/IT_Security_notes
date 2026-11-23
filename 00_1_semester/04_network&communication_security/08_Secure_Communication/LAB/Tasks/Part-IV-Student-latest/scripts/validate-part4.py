"""Read-only baseline checks plus temporary, automatically removed traffic probes."""
import json
import subprocess
from pathlib import Path
import sys
BACKEND_PORT = 8080  # Internal Server port; host 8082 belongs to the Router GUI.
READ_ONLY = '--read-only' in sys.argv

def run(*args, ok=True):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ok and p.returncode:
        raise AssertionError(f'{args}: {p.stderr or p.stdout}')
    return p

def ex(host, *args, **kw):
    return run('docker', 'exec', host, *args, **kw)

def check(value, label):
    assert value, label
    print('PASS', label, flush=True)

def tcp(host, ip, port, allowed):
    p = ex(host, 'nc', '-z', '-w', '2', ip, str(port), ok=False)
    check((p.returncode == 0) == allowed, f'{host} -> {ip}:{port} allowed={allowed}')
for host, cidr, gw in [('admin', '10.10.0.10/27', '10.10.0.1'), ('employee', '10.10.0.42/27', '10.10.0.33'), ('server', '10.10.0.74/27', '10.10.0.65'), ('guest', '10.10.0.106/27', '10.10.0.97'), ('printer', '10.10.0.138/27', '10.10.0.129')]:
    addresses = json.loads(ex(host, 'ip', '-j', '-4', 'addr', 'show', 'dev', 'eth0').stdout)[0]['addr_info']
    check([f"{a['local']}/{a['prefixlen']}" for a in addresses] == [cidr], host + ' address')
    defaults = json.loads(ex(host, 'ip', '-j', 'route', 'show', 'default').stdout)
    check(len(defaults) == 1 and defaults[0]['gateway'] == gw, host + ' gateway')
for iface, cidr in [('eth0', '172.30.255.2/24'), ('eth1', '10.10.0.1/27'), ('eth2', '10.10.0.33/27'), ('eth3', '10.10.0.65/27'), ('eth4', '10.10.0.97/27'), ('eth5', '10.10.0.129/27')]:
    check(cidr in ex('router', 'ip', '-o', '-4', 'addr', 'show', 'dev', iface).stdout, 'router ' + iface)
check('default via 172.30.255.1 dev eth0' in ex('router', 'ip', 'route').stdout, 'router gateway')
check(ex('router', 'sysctl', '-n', 'net.ipv4.ip_forward').stdout.strip() == '1', 'forwarding')
ex('router', 'iptables', '-t', 'nat', '-C', 'POSTROUTING', '-j', 'MOSEC_NAT')
ex('router', 'iptables', '-t', 'nat', '-C', 'MOSEC_NAT', '-o', 'eth0', '-j', 'MASQUERADE')
check(True, 'NAT')
for external, internal in [(18080, 80), (18443, 443)]:
    ex('router', 'iptables', '-t', 'nat', '-C', 'MOSEC_WEB_ENTRY', '-i', 'eth0', '-d', '172.30.255.2/32', '-p', 'tcp', '--dport', str(external), '-m', 'comment', '--comment', f'web-{internal}', '-j', 'DNAT', '--to-destination', f'10.10.0.74:{internal}')
check(True, 'all host web entries DNAT to Server through Router')
expected = json.loads(Path('router/part3-policy.json').read_text())
for rule in expected:
    ex('router', 'iptables', '-C', 'MOSEC_ACL', *rule)
import shlex
actual = [shlex.split(l)[2:] for l in ex('router', 'iptables', '-S', 'MOSEC_ACL').stdout.splitlines() if l.startswith('-A ')]
check([a[a.index('--comment') + 1] for a in actual] == [a[a.index('--comment') + 1] for a in expected], 'exact inherited rule count and order')
check(ex('router', 'iptables', '-S', 'FORWARD').stdout.splitlines()[0] == '-P FORWARD DROP', 'default forwarding deny')
check(ex('router', 'iptables', '-S', 'FORWARD').stdout.splitlines()[1:] == ['-A FORWARD -j MOSEC_ACL'], 'effective forwarding order')
for args in [('-i', 'lo', '-m', 'comment', '--comment', 'host-loopback', '-j', 'ACCEPT'), ('-s', '10.10.0.10/32', '-p', 'tcp', '--dport', '22', '-m', 'comment', '--comment', 'host-admin-ssh', '-j', 'ACCEPT'), ('-p', 'tcp', '--dport', '22', '-m', 'comment', '--comment', 'host-other-ssh-deny', '-j', 'DROP')]:
    ex('server', 'iptables', '-C', 'INPUT', *args)
check(True, 'Server SSH host firewall')
host_rules = ex('server', 'iptables', '-S', 'INPUT').stdout.splitlines()
check(len(host_rules) == 4 and 'host-loopback' in host_rules[1] and ('host-admin-ssh' in host_rules[2]) and ('host-other-ssh-deny' in host_rules[3]), 'host firewall exact order')
ex('router', 'python', '-c', 'import json,network; rows=network.firewall_rules(); meta=json.load(open("/app/part3-rule-metadata.json")); assert [(r["description"],r["rule_type"]) for r in rows] == [(m["description"],m["type"]) for m in meta]')
check(True, 'GUI reduced rule descriptions and types')
for host in ['admin', 'employee']:
    tcp(host, '10.10.0.74', 22, host == 'admin')
    tcp(host, '10.10.0.74', 80, True)
    tcp(host, '10.10.0.74', BACKEND_PORT, False)
for host in ['admin', 'employee', 'server']:
    check(ex(host, 'curl', '--retry', '2', '--max-time', '20', '-fsS', 'https://example.com', ok=False).returncode == 0, 'Internet ' + host)
members = {}
for host in ['admin', 'employee', 'server', 'guest', 'printer']:
    nets = json.loads(run('docker', 'inspect', host).stdout)[0]['NetworkSettings']['Networks']
    check(len(nets) == 1, host + ' single LAN attachment')
    members[host] = set(nets)
check(len(set.union(*members.values())) == 5, 'five genuinely separate L2 LANs')
for host in ['guest', 'printer']:
    for port in [22, 80, BACKEND_PORT]:
        tcp(host, '10.10.0.74', port, False)
for host in ['admin', 'employee']:
    tcp(host, '10.10.0.74', 443, False)
if not READ_ONLY:
    import time
    probes = []
    try:
        for host, port in [('admin', 17841), ('employee', 17842), ('server', 443)]:
            probes.append(subprocess.Popen(['docker', 'exec', host, 'timeout', '25', 'nc', '-lk', '-p', str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        time.sleep(0.5)
        tcp('server', '10.10.0.10', 17841, False)
        tcp('server', '10.10.0.42', 17842, False)
        tcp('server', '127.0.0.1', 443, True)
        for host in ['admin', 'employee', 'guest', 'printer']:
            tcp(host, '10.10.0.74', 443, False)
        tcp('router-gui', '172.30.255.2', 18443, False)
        tcp('employee', '10.10.0.10', 17841, False)
        tcp('admin', '10.10.0.42', 17842, False)
    finally:
        for p in probes:
            p.wait(timeout=30)

def counter(chain, label):
    return int(next((l.split()[0] for l in ex('router', 'iptables', '-t', 'nat', '-L', chain, '-nvx').stdout.splitlines() if '/* ' + label + ' */' in l)))
for host_port, server_port in [(8080, 80), (80, 80), (443, 443)]:
    before = counter('MOSEC_WEB_ENTRY', 'web-' + str(server_port))
    snat = counter('MOSEC_WEB_SNAT', 'web-return-path')
    p = run('curl', '--noproxy', '*', '--max-time', '3', '-ksS',
            ('https' if server_port == 443 else 'http') + '://127.0.0.1:' + str(host_port), ok=False)
    check(counter('MOSEC_WEB_ENTRY', 'web-' + str(server_port)) > before, 'host traffic passes Router DNAT')
    check((p.returncode == 0) == (server_port == 80), 'HTTP only host entry')
    if server_port == 80:
        check(counter('MOSEC_WEB_SNAT', 'web-return-path') > snat, 'SNAT return path')
check(f'0.0.0.0:{BACKEND_PORT} ' in ex('server', 'ss', '-lnt').stdout, 'backend wildcard listener')
for host in ['server']:
    check(':443 ' not in ex(host, 'ss', '-lnt').stdout, 'no TLS listener ' + host)
ex('server', 'test', '-d', '/etc/nginx/certs')
ex('server', 'test', '-d', '/etc/nginx/private')
check(ex('server', 'find', '/etc/nginx/certs', '/etc/nginx/private', '-type', 'f').stdout == '', 'certificate/key directories exist and are empty')
ex('server', 'nginx', '-t')
check(True, 'nginx baseline syntax')
check(ex('server', 'cat', '/etc/mosec/portal-bind').stdout.strip() == '0.0.0.0', 'baseline portal binding restored')
nginx = ex('server', 'nginx', '-T').stdout
active = '\n'.join((line.split('#', 1)[0] for line in nginx.splitlines()))
check('Strict-Transport-Security' not in active, 'no HSTS at baseline')
check('ssl_certificate' not in active and 'listen 443' not in active, 'TLS config inactive')
check(f'proxy_pass http://127.0.0.1:{BACKEND_PORT};' in active and '#     listen 443 ssl;' in nginx, 'HTTP proxy ready; HTTPS placeholder present')
check(ex('server', 'cat', '/etc/nginx/conf.d/default.conf').stdout == Path('server/nginx/default.conf').read_text(), 'exact HTTP baseline restored')
print('PART II SOLVED / REDUCED PART III BASELINE / PART IV INFRASTRUCTURE READY, TLS UNSOLVED')
