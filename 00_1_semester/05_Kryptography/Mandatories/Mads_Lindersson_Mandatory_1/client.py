import socket
import sys
import json

server_host = "127.0.0.1"
server_port = 12000

def startConnection():
    try:
        print("username = client1")
        print("password = client1password")
        username = input("Enter username: ")
        password = input("Enter password: ")

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((server_host, server_port))

        json_login = {
            "username": username,
            "password": password
        }

        json_message = json.dumps(json_login).encode("utf-8")
        clientsocket.sendall(json_message)

        server_reply = clientsocket.recv(2048).decode()

        if server_reply == "LOGIN_OK":
            print("Connection established, you can now write messages (type 'q' to quit)")

            while True:
                message = input("-")
                if message == "quit":
                    break
                if message:
                    clientsocket.sendall(message.encode("utf-8"))

            clientsocket.close()
            print("disconnected")
        else:
            print("Connection could not be established")
            clientsocket.close()
    
        
    except:
        print("Connection to server could not be established")
        sys.exit(0)

startConnection()