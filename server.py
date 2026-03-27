import socket
import os

SERVER_IP = "127.0.0.1"
PORT = 15000
CHUNK_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, PORT))

print("Server started...")

#LOAD LAST PROGRESS
last_chunk = -1
if os.path.exists("progress.txt"):
    with open("progress.txt", "r") as f:
        content = f.read().strip()
        if content:
            last_chunk = int(content)

# IMPORTANT: use append mode for resume
file = open("received_file.txt", "ab")

while True:
    packet, addr = server.recvfrom(CHUNK_SIZE + 10)

    # HANDLE RESUME REQUEST
    if packet == b"RESUME":
        server.sendto(str(last_chunk).encode(), addr)
        continue

    if packet == b"END":
        break

    # extract sequence number
    seq = int(packet[:6].decode())
    chunk = packet[6:]

    file.write(chunk)

    #SAVE PROGRESS
    last_chunk = seq
    with open("progress.txt", "w") as f:
        f.write(str(last_chunk))

    print("Received chunk", seq)

file.close()

print("File received successfully")