import socket
import json
import bcrypt

server_host = "127.0.0.1"
server_port = 12000
accounts = {"client1": '$2b$16$u6ICB8a/Iu8WuXvacZMXq.EVbxWnhM/SJCjHOXstjw4sB4VJsNwa6'}

def createServer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((server_host, server_port))
    serversocket.listen(1)
    serversocket.settimeout(1.0)
    print("server has startet")
    while True:
        try:
            (clientsocket, address) = serversocket.accept()
            print("Connection from:", address)
            request = clientsocket.recv(2048).decode()
            login = validateLogin(request)

            if login[0]:
                print("Client:", login[1], "has connected")
                clientsocket.sendall("LOGIN_OK".encode("utf-8"))

                try:
                    while True:
                        message = clientsocket.recv(2048).decode()
                        if not message:
                            print("Client disconected")
                            break
                        print(login[1], ":", message)
                except Exception:
                    print("Client disconnected")
                finally:
                    clientsocket.close()
            else:
                print("Client tried to connect, but had bad login")
                clientsocket.sendall("LOGIN_FAILED".encode("utf-8"))
                clientsocket.close()
            
        except socket.timeout:
            continue

def validateLogin(request):
    loginCred = unpackRequestToLogin(request)

    if loginCred[0] not in accounts:
        return [False, None]
    
    if bcrypt.checkpw(loginCred[1].encode("utf-8"), accounts[loginCred[0]].encode("utf-8")):
        return [True, loginCred[0]]
    else:
        return [False, None]

def unpackRequestToLogin(request):
    data = json.loads(request)

    username = data.get("username")
    password = data.get("password")

    return [username, password]

createServer()