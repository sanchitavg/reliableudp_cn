import socket

SERVER_IP = "127.0.0.1"
PORT = 15000
CHUNK_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

file = open("file.txt", "rb")

seq = 0  # sequence number

while True:
    chunk = file.read(CHUNK_SIZE)

    if not chunk:
        break

    # add sequence number (6 digits)
    packet = f"{seq:06}".encode() + chunk

    client.sendto(packet, (SERVER_IP, PORT))

    print("Sent chunk", seq)

    seq += 1

file.close()

client.sendto(b"END", (SERVER_IP, PORT))

print("File sent successfully")