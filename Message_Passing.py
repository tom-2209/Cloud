### SERVER CODE 
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []

def handle_client(conn, addr):
    print("Connected:", addr)

    while True:
        try:
            message = conn.recv(1024).decode()

            if not message or message.lower() == "exit":
                break

            print(f"Client {addr}: {message}")

            # Broadcast message to all other clients
            for client in clients[:]:
                if client != conn:
                    try:
                        client.sendall(
                            f"Client {addr}: {message}".encode()
                        )
                    except OSError:
                        clients.remove(client)

        except OSError:
            break

    if conn in clients:
        clients.remove(conn)

    conn.close()
    print("Disconnected:", addr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("Server started. Waiting for clients...")

try:
    while True:
        conn, addr = server.accept()
        clients.append(conn)

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()

except KeyboardInterrupt:
    print("\nServer shutting down.")

finally:
    server.close()



### CLIENT CODE

import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print("\nReceived:", message)

        except OSError:
            break

thread = threading.Thread(
    target=receive_messages,
    daemon=True
)
thread.start()

print("Connected to server.")
print("Type a message. Enter 'exit' to quit.")

try:
    while True:
        message = input("You: ")

        client.sendall(message.encode())

        if message.lower() == "exit":
            break

finally:
    client.close()

