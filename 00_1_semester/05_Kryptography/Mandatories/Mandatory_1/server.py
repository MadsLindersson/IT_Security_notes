import socket

server_host = "localhost"
server_port = 12000
list_of_clients = []

def createServer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((server_host, server_port))
    serversocket.listen(1)
    print("server has startet")
    while True:
        (clientsocket, address) = serversocket.accept()
        print("Connection from:", address)
        request = clientsocket.recv(2048).decode()
        
        clientsocket.close()

createServer()