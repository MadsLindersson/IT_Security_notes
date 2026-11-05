import socket
import functions

server_host = "0.0.0.0"
server_port = 12000

def createServer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((server_host, server_port))
    serversocket.listen(1)
    print("server has startet")
    while True:
        (clientsocket, address) = serversocket.accept()
        print("Connection from:", address)
        request = clientsocket.recv(2048).decode()
        
        try:
            clientsocket.send(functions.fetch_http_response(functions.get_requested_page_name(request), request, address).encode())
        except:
            with open("400.html", "r") as f:
                clientsocket.send(f"HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n{f.read()}".encode())
                try:
                    if functions.get_requested_page_name(request) != "/.well-known/appspecific/com.chrome.devtools.json":
                        functions.create_log_entry(request, address, "400", "400.html")
                except:
                    print("Unable to log")
        
        clientsocket.close()

createServer()