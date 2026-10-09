import socket

mysock = socket.socket()

try:
    mysock.connect(("127.0.0.1", 1450))
except Exception as e:
    mysock.close()
    exit(f"server is down try again later {str(e)}")


while True:
    msg = input("enter time/name/rand to get something or exit to finish: ")

    if len(msg) == 4 and msg in ["exit","time","name","rand"]:

        if msg.lower() == "exit":
            try:
                mysock.send(msg.encode())
            except Exception as e:
                print(f"error in receiving or sending data {str(e)}")
            break

        else:
            try:
                mysock.send(msg.encode())
                data_length = mysock.recv(2).decode()
                data = mysock.recv(int(data_length)).decode()
                print(f"server send - {data}")
            except Exception as e:
                print(f"error in receiving or sending data {str(e)}")
                break

    else:
        print("the length of the message is wrong, pls try another message")

mysock.close()