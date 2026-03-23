import socket

SERVER_IP = "127.0.0.1"
PORT = 15000
CHUNK_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, PORT))

print("Server started...")

file = open("received_file.txt", "wb")

while True:
    packet, addr = server.recvfrom(CHUNK_SIZE + 10)

    if packet == b"END":
        break

    # extract sequence number
    seq = int(packet[:6].decode())
    chunk = packet[6:]

    file.write(chunk)

    print("Received chunk", seq)

file.close()

print("File received successfully")