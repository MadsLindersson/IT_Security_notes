import select
import socket
import socketserver
import threading


TARGETS = {8082: 8080, 8080: 18080, 80: 18080, 443: 18443}


class ProxyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        upstream = socket.create_connection(("172.30.255.2", self.server.target_port), timeout=5)
        sockets = [self.request, upstream]
        try:
            while True:
                readable, _, _ = select.select(sockets, [], [], 30)
                if not readable:
                    break
                for sock in readable:
                    data = sock.recv(65536)
                    if not data:
                        return
                    target = upstream if sock is self.request else self.request
                    target.sendall(data)
        finally:
            upstream.close()


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


# Publish through this existing single-network relay. TLS bytes pass unchanged.
servers = []
try:
    for local_port, target_port in TARGETS.items():
        server = ThreadingTCPServer(("0.0.0.0", local_port), ProxyHandler)
        server.target_port = target_port
        servers.append(server)
        threading.Thread(target=server.serve_forever, daemon=True).start()
    threading.Event().wait()
finally:
    for server in servers:
        server.shutdown()
        server.server_close()
