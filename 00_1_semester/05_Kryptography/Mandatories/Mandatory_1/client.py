import socket

server_host = "localhost"
server_port = 12000

def startServer():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.bind((server_host, server_port))
    clientsocket.listen(1)
    print("server has startet")
    while True:
        (clientsocket, address) = clientsocket.accept()
        print("Connection from:", address)
        request = clientsocket.recv(2048).decode()
        
        clientsocket.close()

startServer()