from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(("localhost", 8081))

file = open("image/pomeranian.jpeg", "rb")
file_chunk = file.read(2048)

while file_chunk:
    client.send(file_chunk)
    file_chunk = file.read(2048)

file.close()
client.close()
