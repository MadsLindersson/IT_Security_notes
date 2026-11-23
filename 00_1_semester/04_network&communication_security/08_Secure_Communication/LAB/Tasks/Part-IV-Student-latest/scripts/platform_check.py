"""Check the Docker server, not the host OS; no Desktop APIs are used."""
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def output(*args):
    return subprocess.check_output(args, text=True, cwd=ROOT).strip()


def check():
    version = output('docker', 'compose', 'version', '--short')
    numbers = tuple(map(int, re.search(r'(\d+)\.(\d+)\.(\d+)', version).groups()))
    if numbers < (2, 36, 0):
        raise RuntimeError('Docker Compose V2 2.36.0+ required for interface_name and gw_priority')
    info = json.loads(output('docker', 'info', '--format', '{{json .}}'))
    arch = {'aarch64': 'arm64', 'arm64': 'arm64', 'x86_64': 'amd64', 'amd64': 'amd64'}.get(info.get('Architecture'))
    if info.get('OSType') != 'linux' or not arch:
        raise RuntimeError('Use a Linux Docker Engine on AMD64 or ARM64')
    if int(info['ServerVersion'].split('.')[0]) < 28:
        raise RuntimeError('Docker Engine 28+ required for gateway priority')
    if any('rootless' in option for option in info.get('SecurityOptions', [])):
        raise RuntimeError('This routing lab requires rootful Docker Engine')
    if os.environ.get('DOCKER_DEFAULT_PLATFORM', 'linux/' + arch) != 'linux/' + arch:
        raise RuntimeError('Unset DOCKER_DEFAULT_PLATFORM to build for the native Docker server architecture')
    # Avoid resetting the identically named Part III project from another checkout.
    ids = output('docker', 'ps', '-aq', '--filter', 'label=com.docker.compose.project=mosec-router-lab').split()
    if ids:
        for container in json.loads(output('docker', 'inspect', *ids)):
            owner = container['Config']['Labels'].get('com.docker.compose.project.working_dir', '')
            if Path(owner).resolve() != ROOT:
                raise RuntimeError('Lab containers belong to another checkout: ' + owner)
    subprocess.run(['docker', 'compose', 'config', '--quiet'], cwd=ROOT, check=True)
    print('Docker server: linux/' + arch + '; Compose ' + version)


if __name__ == '__main__':
    try:
        check()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
