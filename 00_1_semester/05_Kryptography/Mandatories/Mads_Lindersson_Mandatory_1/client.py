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
        
        json_message = json.dumps(json_login)
        encrypted_json = encrypt_message(json_message)
        clientsocket.sendall(encrypted_json.encode("utf-8"))

        server_reply = json.loads(decrypt_message(clientsocket.recv(2048).decode()))

        if server_reply.get("status") == "LOGIN_OK":
            print("Connection established, you can now write messages (type 'q' to quit)")
            shift = server_reply.get("shift")
            while True:
                message = input("-")
                if message == "quit":
                    break
                if message:
                    encrypted_msg = encrypt_message(message, shift)
                    clientsocket.sendall(encrypted_msg.encode("utf-8"))

            clientsocket.close()
            print("disconnected")
        else:
            print("Connection could not be established")
            clientsocket.close()
    
    except:
        print("Connection to server could not be established")
        sys.exit(0)

def encrypt_message(msg, shift=3):
    result = ""
    for char in msg:
        ascii_num = ord(char)
        if 32 <= ascii_num <= 126:
            result += chr((ascii_num - 32 + shift) % 95 + 32)
        else:
            result += char
    return result

def decrypt_message(msg, shift=3):
    result = ""
    for char in msg:
        ascii_num = ord(char)
        if 32 <= ascii_num <= 126:
            result += chr((ascii_num - 32 - shift) % 95 + 32)
        else:
            result += char
    return result

startConnection()