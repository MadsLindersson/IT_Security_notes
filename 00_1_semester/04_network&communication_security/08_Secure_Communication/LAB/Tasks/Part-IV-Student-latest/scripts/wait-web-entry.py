"""Verify host publication after container recreation, on Docker Engine."""
import subprocess
import time


def ready():
    for port, marker in [(8082,'password'), (8080,'name="password"'), (80,'name="password"')]:
        p=subprocess.run(['curl','--noproxy','*','--max-time','2','-fsS',f'http://127.0.0.1:{port}/login'],
                         text=True,capture_output=True)
        if p.returncode or marker not in p.stdout:
            return False
    return True


def wait():
    for _ in range(10):
        if ready():
            return True
        time.sleep(1)
    return False


if not wait():
    # Container health does not check the host port publication.
    # Recreate only this project's relay once; never change global Docker state.
    print('Refreshing lab relay: published HTTP entry not ready',flush=True)
    subprocess.run(['docker','compose','up','-d','--no-deps','--force-recreate','router-gui'],check=True)
    if not wait():
        raise SystemExit('Host HTTP entry unavailable after relay recreation (8080/8082/80)')
print('Host HTTP entry points ready',flush=True)
