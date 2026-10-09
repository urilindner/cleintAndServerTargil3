import socket
import random
import time
server_sock = socket.socket()
server_sock.bind(("0.0.0.0" , 1450))
server_sock.listen(3)

while True:
    #server wait for clients

    client_sock,addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    while True:
        #handle one client

        try:
            data = client_sock.recv(4).decode()

        except Exception as e:
            print(f"error in recv/send {str[e]}")
            client_sock.close()
            break

        if data == "":
            break
        print(f"getting data - {data}")
        if data.lower() == "name":
            sendDeta = "UriLindner"

        elif data.lower() == "rand":
            sendDeta = random.randint(1, 11)

        elif data.lower() == "time":
            sendDeta = time.ctime()

        elif data.lower() == "exit":
            print(f"{addr[0]} - disconnected")
            sendDeta = "goodbye"
            lengthDeta = str(len(str(sendDeta))).zfill(2)
            client_sock.send(lengthDeta.encode())
            client_sock.send(sendDeta.encode())
            client_sock.close()
            break

        else:
            print(f"{addr[0]} - kick out")
            client_sock.close()
            break

        lengthDeta = str(len(str(sendDeta))).zfill(2)
        client_sock.send(lengthDeta.encode())
        client_sock.send(str(sendDeta).encode())