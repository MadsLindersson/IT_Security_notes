"""Validate actual Linux links by attachment MAC before configuring teaching IPs."""
import json
import os
import subprocess

expected = dict(item.split('=', 1) for item in os.environ.get('EXPECTED_LINKS', '').split(',') if item)
if not expected:
    # Historical compose.yaml does not opt into dynamic topology management.
    raise SystemExit(0)
links = json.loads(subprocess.check_output(['ip', '-j', 'link'], text=True))
by_mac = {link['address'].lower(): link['ifname'] for link in links if 'address' in link}
for interface, mac in expected.items():
    if by_mac.get(mac) != interface:
        subprocess.run(['sysctl', '-w', 'net.ipv4.ip_forward=0'], check=False)
        raise SystemExit(f'Unsafe interface mapping: {mac} expected {interface}, found {by_mac.get(mac)}')
print('Validated router network MAC/interface mapping:', expected, flush=True)
