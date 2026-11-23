"""Host port forwarding only; security policy belongs to the inherited baseline."""
import subprocess
from network import run_cmd, wan_name


def reset_chain(table, chain, parent):
    prefix = ['iptables', '-t', table]
    subprocess.run([*prefix, '-N', chain], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run_cmd([*prefix, '-F', chain])
    while subprocess.run([*prefix, '-C', parent, '-j', chain], capture_output=True).returncode == 0:
        run_cmd([*prefix, '-D', parent, '-j', chain])
    run_cmd([*prefix, '-I', parent, '1', '-j', chain])


reset_chain('nat', 'MOSEC_WEB_ENTRY', 'PREROUTING')
for external, destination, internal in [(18080, '10.10.0.74', 80), (18443, '10.10.0.74', 443)]:
    run_cmd(['iptables', '-t', 'nat', '-A', 'MOSEC_WEB_ENTRY', '-i', wan_name(),
             '-d', '172.30.255.2/32', '-p', 'tcp', '--dport', str(external),
             '-m', 'comment', '--comment', f'web-{internal}',
             '-j', 'DNAT', '--to-destination', f'{destination}:{internal}'])

# Docker's bridge NAT can otherwise rewrite a management-network source to its
# bootstrap gateway while crossing Server LAN. Keep both directions at the router.
reset_chain('nat', 'MOSEC_WEB_SNAT', 'POSTROUTING')
for destination, ports in [('10.10.0.74', '80,443')]:
    run_cmd(['iptables', '-t', 'nat', '-A', 'MOSEC_WEB_SNAT', '-o', 'eth3',
             '-d', destination + '/32', '-p', 'tcp', '-m', 'multiport', '--dports', ports,
             '-m', 'conntrack', '--ctstate', 'DNAT', '-m', 'comment', '--comment',
             'web-return-path', '-j', 'SNAT', '--to-source', '10.10.0.65'])

# Filtering lives in part3-policy.json; NAT never grants HTTPS permission.
subprocess.run(['iptables', '-D', 'FORWARD', '-j', 'MOSEC_WAN_ENTRY'], capture_output=True)
subprocess.run(['iptables', '-F', 'MOSEC_WAN_ENTRY'], capture_output=True)
subprocess.run(['iptables', '-X', 'MOSEC_WAN_ENTRY'], capture_output=True)
