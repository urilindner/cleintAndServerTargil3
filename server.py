import socket
import random
import time
from PIL import ImageGrab
import pyperclip
import subprocess
import shutil
import os

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
            lnData = client_sock.recv(2).decode()
            data = client_sock.recv(int(lnData)).decode()

        except Exception as e:
            print(f"error in recv/send {str[e]}")
            client_sock.close()
            break

        if data == "":
            break
        print(f"getting data - {data}")

        if data.lower() == "printscreen":
            im = ImageGrab.grab()
            im.save(r'screen.jpg')
            sendDeta = 'screen.jpg'

        elif data.lower().startswith("copyclip: "):
            textToCopy = data[10:]
            pyperclip.copy(textToCopy)
            sendDeta = "Copied to clipboard successfully"


        elif data.lower() == "pasteclip":
            sendDeta = pyperclip.paste()
            if sendDeta == "":
                sendDeta = "Clipboard is empty"
            print(f"Sending back: {sendDeta}")


        elif data.lower().startswith("software: "):
            software_name = data[10:]
            try:
                process = subprocess.Popen(software_name)
                sendDeta = "The software was opened"
            except Exception as e:
                sendDeta = "The software wasn't opened"

        elif data.lower().startswith("show_file: ") :
            file_place = data[11:]
            try:
                files_list = os.listdir(file_place)
                sendDeta = ""
                for file in files_list:
                    sendDeta += file
                    sendDeta += ", "
            except FileNotFoundError:
                sendDeta = "Error: The folder path does not exist."

        elif data.lower().startswith("delete_file: "):
            file_name = data[13:]
            if os.path.exists(file_name):
                os.remove(file_name)
                sendDeta = f"File {file_name} deleted successfully"
            else:
                sendDeta = "File not found"

        elif data.lower().startswith("copy_file: "):
            try:
                paths = data[11:].split(">")
                shutil.copy(paths[0], paths[1])
                sendDeta = "File copied successfully"
            except Exception as e:
                sendDeta = f"Copy failed: {str(e)}"

        elif data.lower() == "exit":
            print(f"{addr[0]} - disconnected")
            break

        else:
            print(f"{addr[0]} - kick out")
            client_sock.close()
            break

        lengthDeta = str(len(str(sendDeta))).zfill(2)
        client_sock.send(lengthDeta.encode())
        client_sock.send(str(sendDeta).encode()) #