import socket
import ssl

HOST = input("Enter domain to test (e.g. ek.dk): ").strip()
PORT = 443

# Deliberately obsolete / unsuitable cipher suites.
# The server is very unlikely to accept these.
OLD_CIPHERS = [
    "ADH-AES128-SHA",
    "AECDH-AES128-SHA",
    "DES-CBC3-SHA",
    "RC4-SHA",
]

print(f"\nTarget: {HOST}:{PORT}")
print("Testing deliberately outdated cipher suites...\n")

for cipher in OLD_CIPHERS:

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Force TLS 1.2 so we are testing traditional TLS cipher suites
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2

    # Certificate verification isn't the point of this exercise
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        # SECLEVEL=0 allows some legacy ciphers in newer OpenSSL versions
        context.set_ciphers(cipher + ":@SECLEVEL=0")

    except ssl.SSLError:
        print(f"[LOCAL OPENSSL REJECTED] {cipher}")
        continue

    print(f"Offering ONLY: {cipher}")

    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as tls:

                print("  -> Handshake SUCCEEDED")
                print("  -> Negotiated:", tls.version(), tls.cipher())

    except ssl.SSLError as e:
        print("  -> TLS HANDSHAKE FAILED")
        print("  ->", e)

    except Exception as e:
        print("  -> Connection error:", e)

    print()