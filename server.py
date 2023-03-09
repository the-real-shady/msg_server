import socket
import threading
import datetime

# Define server constants
HOST = "192.168.1.21"  # Your local ip
PORT = 5555
ADDR = (HOST, PORT)
FORMAT = 'utf-8'


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)


clients = []


def handle_client(client_socket, client_address):
    clients.append(client_socket)
    print(f"[NEW CONNECTION] {client_address} connected at {datetime.datetime.now().strftime('%H:%M:%S')}")
    broadcast(f"[NEW CONNECTION] {client_address} connected at {datetime.datetime.now().strftime('%H:%M:%S')}")
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            if message:
                print(f"[{client_address}] {message}")
                broadcast(f"[{client_address}] {message}")
            else:
                clients.remove(client_socket)
                print(f"[DISCONNECTED] {client_address} disconnected at {datetime.datetime.now().strftime('%H:%M:%S')}")
                broadcast(f"[DISCONNECTED] {client_address} disconnected at {datetime.datetime.now().strftime('%H:%M:%S')}")
                client_socket.close()
                break
        except:
            clients.remove(client_socket)
            print(f"[DISCONNECTED] {client_address} disconnected at {datetime.datetime.now().strftime('%H:%M:%S')}")
            broadcast(f"[DISCONNECTED] {client_address} disconnected at {datetime.datetime.now().strftime('%H:%M:%S')}")
            client_socket.close()
            break

def broadcast(message):
    for client_socket in clients:
        client_socket.send(message.encode(FORMAT))

def start():
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()
