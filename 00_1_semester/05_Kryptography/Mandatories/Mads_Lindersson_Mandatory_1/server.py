import socket
import json
import bcrypt

server_host = "127.0.0.1"
server_port = 12000
shift = 5
accounts = {"client1": '$2b$16$u6ICB8a/Iu8WuXvacZMXq.EVbxWnhM/SJCjHOXstjw4sB4VJsNwa6'}

def createServer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((server_host, server_port))
    serversocket.listen(1)
    serversocket.settimeout(1.0) #Timeout er nødsaget for at kunne lukke serveren med CTRL + C i terminalen.
    print("server has startet")
    while True:
        try:
            (clientsocket, address) = serversocket.accept()
            print("Connection from:", address)
            request_decoded = clientsocket.recv(2048).decode()
            request_decrypted = decrypt_message(request_decoded)
            login = validateLogin(request_decrypted)

            if login[0]:
                print("Client:", login[1], "has connected")

                msg = {
                    "status": "LOGIN_OK",
                    "shift": shift
                }

                json_msg = json.dumps(msg)
                msg_encrypted = encrypt_message(json_msg)
                clientsocket.sendall(msg_encrypted.encode("utf-8"))

                try:
                    while True:
                        message = clientsocket.recv(2048).decode()
                        decrypted_message = decrypt_message(message, shift)
                        if not message:
                            print("Client disconected")
                            break
                        print(login[1], ":", decrypted_message)
                except Exception as e:
                    print(f"Something went wrong: {e}")
                finally:
                    clientsocket.close()
            else:
                print("Client tried to connect, but had bad login")
                failed_msg = json.dumps({"status": "LOGIN_FAILED"})
                clientsocket.sendall(encrypt_message(failed_msg).encode("utf-8"))
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

createServer()