"""Project: Certificate Generation Lab
Institution: EK – Erhvervsakademi København
Author: moms@ek.dk
"""

import ipaddress
import re

PROJECT_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
DNS_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


def valid_project_name(value):
    return bool(value and PROJECT_RE.fullmatch(value))


def valid_dns_name(value):
    return bool(value and DNS_RE.fullmatch(value))


def valid_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def clean_text(value, max_len=128):
    value = (value or "").strip()
    if len(value) > max_len:
        raise ValueError("Value is too long.")
    if any(ch in value for ch in "\r\n/\\;&|$`"):
        raise ValueError("Value contains unsupported characters.")
    return value


def clean_days(value, default=3650):
    if value in (None, ""):
        return default
    try:
        days = int(value)
    except (TypeError, ValueError):
        raise ValueError("Lifetime must be a number of days.")
    if days < 1 or days > 10000:
        raise ValueError("Lifetime must be between 1 and 10000 days.")
    return days


def validate_algorithm(value, allowed=None):
    allowed = allowed or {"rsa2048", "rsa3072", "rsa4096", "ecp256"}
    if value not in allowed:
        raise ValueError("Unsupported key algorithm.")
    return value


def validate_dns_list(values):
    cleaned = []
    for item in values or []:
        item = (item or "").strip()
        if not item:
            continue
        if not valid_dns_name(item):
            raise ValueError(f"Invalid DNS SAN: {item}")
        cleaned.append(item)
    return cleaned


def validate_ip_list(values):
    cleaned = []
    for item in values or []:
        item = (item or "").strip()
        if not item:
            continue
        if not valid_ip(item):
            raise ValueError(f"Invalid IP SAN: {item}")
        cleaned.append(item)
    return cleaned
