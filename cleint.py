import socket
from PIL import Image
import pyperclip
import subprocess
import shutil
import os

mysock = socket.socket()

try:
    mysock.connect(("127.0.0.1", 1450))
except Exception as e:
    mysock.close()
    exit(f"server is down try again later {str(e)}")


while True:
    msg = input("enter printscreen/pasteclip/copyclip: text/delete_file: file_path/show_file: file_path/software: software/copy_file: file_path1 > file_path2 to get something or exit to finish: ")

    if msg.lower() in ["printscreen", "pasteclip", "exit"] or msg.lower().startswith(("copyclip: ", "delete_file: ", "copy_file: ", "show_file: ",  "software: ")):

        try:
             length_str = str(len(msg)).zfill(2)
             mysock.send(length_str.encode())
             mysock.send(msg.encode())
        except Exception as e:
            print(f"error in receiving or sending data {str(e)}")
            break

        try:
            data_length = mysock.recv(2).decode()
            data = mysock.recv(int(data_length)).decode()
        except Exception as e:
            print(f"error in receiving or sending data {str(e)}")
            break

        if msg.lower() == "printscreen":
            im = Image.open(data)
            im.show()

        else:
            print(data)

    else:
        print("the message is wrong, pls try another message")

mysock.close() #