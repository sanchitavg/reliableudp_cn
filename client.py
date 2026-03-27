import socket
import time

SERVER_IP = "127.0.0.1"
PORT = 15000
CHUNK_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ASK SERVER WHERE TO RESUME
client.sendto(b"RESUME", (SERVER_IP, PORT))
last_chunk, _ = client.recvfrom(1024)

# handle empty progress
try:
    start_chunk = int(last_chunk.decode()) + 1
except:
    start_chunk = 0

print("Resuming from chunk", start_chunk)

file = open("file.txt", "rb")

#SKIP ALREADY SENT DATA
file.seek(start_chunk * CHUNK_SIZE)

seq = start_chunk  # start from correct chunk

while True:
    chunk = file.read(CHUNK_SIZE)

    if not chunk:
        break

    # add sequence number (6 digits)
    packet = f"{seq:06}".encode() + chunk

    client.sendto(packet, (SERVER_IP, PORT))

    print("Sent chunk", seq)

    time.sleep(0.2)   #  delay for demo - this can be adjusted

    seq += 1

file.close()

client.sendto(b"END", (SERVER_IP, PORT))

# if all chunks have been sent:
if seq == start_chunk:
    print("No new data to send (file already fully transferred)")

print("File sent successfully")