"""Unsolved Part IV baseline checks."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--read-only', action='store_true', help='No packet captures or temporary listeners')
ARGS = PARSER.parse_args()
PASSED = 0


def run(*args, ok=True, **kwargs):
    p = subprocess.run(args, text=True, capture_output=True, cwd=ROOT, timeout=kwargs.pop('timeout', 30), **kwargs)
    if ok and p.returncode:
        raise AssertionError(f'{args}: {p.stdout} {p.stderr}')
    return p


def ex(host, *args, **kwargs):
    return run('docker', 'exec', host, *args, **kwargs)


def passed(label):
    global PASSED
    PASSED += 1
    print('[PASS]', label, flush=True)


def request(path='/', *, host=None, base='http://127.0.0.1:8080', data=None, cookie=None, tls=None, method=None):
    args = ['curl', '--noproxy', '*', '--max-time', '6', '-si']
    if tls:
        args += ['--cacert', str(tls), '--resolve', 'mosec.test:443:127.0.0.1']
    if data is not None:
        args += ['--data', data]
    if cookie:
        args += ['--cookie', cookie]
    if method:
        args += ['-X', method]
    args += [base + path]
    p = ex(host, *args) if host else run(*args)
    headers, _, body = p.stdout.partition('\n\n')
    status = int(headers.splitlines()[0].split()[1])
    return status, headers, body


def authentication(**kw):
    assert request(**kw)[0] == 200
    status, _, form = request('/login', **kw)
    assert status == 200 and 'name="username"' in form and 'name="password"' in form
    assert 'application/x-www-form-urlencoded' in form
    assert 'alice123' not in form and 'bob123' not in form
    for path, mime in [('/static/css/main.css','text/css'),('/static/js/main.js','text/javascript')]:
        status, headers, body = request(path, **kw)
        assert status == 200 and mime in headers and body.strip()
    for path in ['/dashboard','/profile']:
        status, headers, _ = request(path, **kw)
        assert status == 303 and 'Location: /login' in headers
    for name, password, full_name, student_id, other_name, attendance in [
        ('alice','alice123','Alice Jensen','STU-2026-1042','Bob Nielsen',92),
        ('bob','bob123','Bob Nielsen','STU-2026-1088','Alice Jensen',86),
    ]:
        status, headers, _ = request('/login', data=f'username={name}&password={password}', **kw)
        assert status == 303 and 'Location: /dashboard' in headers, (status, headers)
        cookie = re.search(r'(?im)^Set-Cookie:\s*([^;]+)', headers).group(1)
        status, _, body = request('/dashboard', cookie=cookie, **kw)
        assert status == 200 and full_name in body and student_id in body and other_name not in body
        assert f'value="{attendance}"' in body
        for label in ['Upcoming meetings','Completed tasks','Notifications','Attendance']:
            assert label in body
        status, _, body = request('/profile', cookie=cookie, **kw)
        assert status == 200 and full_name in body and student_id in body and other_name not in body
        assert f'{name}.student@example.test' in body
        assert request('/logout', cookie=cookie, method='POST', **kw)[0] == 303
        for path in ['/dashboard','/profile']:
            status, headers, _ = request(path, cookie=cookie, **kw)
            assert status == 303 and 'Location: /login' in headers
    status, _, error = request('/login', data='username=alice&password=wrong', **kw)
    assert status == 401 and 'Invalid username or password' in error and 'name="password"' in error
    assert request('/login', data='username=charlie&password=charlie123', **kw)[0] == 401


def baseline():
    args = ['python3', str(ROOT/'scripts/validate-part4.py')]
    if ARGS.read_only:
        args += ['--read-only']
    p = run(*args, timeout=240)
    assert 'PART II SOLVED / REDUCED PART III BASELINE' in p.stdout
    passed('/27 routing, NAT and reduced ACL/Firewall/state/SSH baseline')
    ex('server', 'curl', '--noproxy', '*', '--retry', '2', '--retry-all-errors', '--retry-delay', '1', '--connect-timeout', '8', '--max-time', '15', '-fsS', 'https://example.com/', timeout=55)
    passed('Server outbound Internet through inherited policy and NAT')
    assert '0.0.0.0:8080 ' in ex('server', 'ss', '-lnt').stdout
    for host in ['admin', 'employee']:
        authentication(host=host, base='http://10.10.0.74')
    authentication()
    authentication(base='http://127.0.0.1:80')
    authentication(host='server', base='http://127.0.0.1:8080')
    assert request('/login', base='http://127.0.0.1:8082')[0] == 200
    passed('Portal accounts, sessions, CSS/JS through Nginx; GUI on 8082')
    config = json.loads(run('docker', 'compose', 'config', '--format', 'json').stdout)
    healthcheck = config['services']['server']['healthcheck']['test']
    assert 'http://localhost:8080 ' in healthcheck[-1], 'Server healthcheck backend port'
    for host in ['server', 'router']:
        health = json.loads(run('docker', 'inspect', host).stdout)[0]['State']['Health']
        assert health['Status'] == 'healthy', (host, health)
    assert not config['services']['server'].get('ports')
    ports = config['services']['router-gui']['ports']
    assert {(p['host_ip'], str(p['published']), p['target']) for p in ports} == {('127.0.0.1','8080',8080),('127.0.0.1','8082',8082),('127.0.0.1','80',80),('127.0.0.1','443',443)}
    for host in ['server', 'router']:
        assert json.loads(run('docker', 'inspect', host).stdout)[0]['HostConfig']['PortBindings'] in ({}, None)
    for host, bindings in [('router-gui', {'8080/tcp':'8080', '8082/tcp':'8082', '80/tcp':'80', '443/tcp':'443'})]:
        actual=json.loads(run('docker','inspect',host).stdout)[0]['HostConfig']['PortBindings']
        assert set(actual)==set(bindings)
        for port, value in actual.items():
            assert value==[{'HostIp':'127.0.0.1','HostPort':bindings[port]}]
    passed('Loopback GUI and Nginx entries; no conflicting mappings')
    ex('server', 'nginx', '-t')
    for directory in ['/etc/nginx/certs', '/etc/nginx/private']:
        ex('server', 'test', '-d', directory)
        assert ex('server', 'find', directory, '-type', 'f').stdout == ''
    assert ':443 ' not in ex('server','ss','-lnt').stdout
    probe = run('curl','--noproxy','*','--max-time','4','-ksS','https://127.0.0.1:443/',ok=False)
    assert probe.returncode != 0, 'Host 443 unexpectedly serves HTTPS'
    assert len(config['services']) == 7
    status = ex('server','supervisorctl','status').stdout
    assert all(any(line.startswith(name+' ') and 'RUNNING' in line for line in status.splitlines()) for name in ['portal','nginx','sshd','udp'])
    passed('HTTP proxy and empty certificate/key directories; host 443 has no working TLS')


def main():
    baseline()
    print(f'Result: {PASSED}/{PASSED} PASS', flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        import traceback
        frame = traceback.extract_tb(error.__traceback__)[-1]
        print('[FAIL]', f'{frame.filename}:{frame.lineno}: {error}', flush=True)
        print(f'Result: {PASSED}/{PASSED+1} PASS', flush=True)
        raise SystemExit(1)
