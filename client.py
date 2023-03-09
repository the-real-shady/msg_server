import socket
import threading

# Define client constants
HOST = "192.168.1.21"
PORT = 5555
ADDR = (HOST, PORT)
FORMAT = 'utf-8'


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)


def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            print(message)
        except:
            break


def send():
    while True:
        message = input()
        client_socket.send(message.encode(FORMAT))


receive_thread = threading.Thread(target=receive)
receive_thread.start()


send_thread = threading.Thread(target=send)
send_thread.start()
