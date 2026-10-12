#Server Code
import socket

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server is waiting for a client...")

conn, addr = server.accept()
print("Connected to:", addr)

data = conn.recv(1024).decode()
print("Received numbers:", data)

numbers = list(map(int, data.split()))
total = sum(numbers)

conn.send(str(total).encode())
print("Sum sent:", total)

conn.close()
server.close()



#client Code

import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

message = input("Enter numbers separated by spaces: ")
client.send(message.encode())

response = client.recv(1024).decode()
print("Sum received from server:", response)

client.close()



####################################################
Save the first program as server.py.



Save the second program as client.py.

Open two terminals in the same folder.

Run the server first:
python server.py

Run the client in the second terminal:
python client.py

