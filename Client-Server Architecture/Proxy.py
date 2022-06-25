from socket import *

import random
import cv2
import os

proxy_server = socket(AF_INET, SOCK_STREAM)
proxy_server.bind(("localhost", 8081))
proxy_server.listen()

client_socket, client_address = proxy_server.accept()

file = open("image/proxy/recv_original_image_proxy.jpeg", "wb")
file_chunk = client_socket.recv(2048)

while file_chunk:
    file.write(file_chunk)
    file_chunk = client_socket.recv(2048)

    if not file_chunk:
        break

file.close()
client_socket.close()


def add_noise(image):
    row, col = image.shape[0], image.shape[1]
    number_of_pixels = random.randint(300, 10000)
    for _ in range(number_of_pixels):
        y_cord = random.randint(0, row - 1)
        x_cord = random.randint(0, col - 1)
        image[y_cord][x_cord] = 255
    for _ in range(number_of_pixels):
        y_cord = random.randint(0, row - 1)
        x_cord = random.randint(0, col - 1)
        image[y_cord][x_cord] = 0
    return image


original_image = cv2.imread("image/proxy/recv_original_image_proxy.jpeg")
print(f"Размер оригинального изображения: {os.path.getsize('image/proxy/recv_original_image_proxy.jpeg')}")
noise_image = add_noise(original_image)
cv2.imwrite("image/proxy/image_noise_on_proxy.jpeg", noise_image)
client_socket.close()
proxy_server_second = socket(AF_INET, SOCK_STREAM)
proxy_server_second.connect(("127.0.0.1", 8080))
file = open("image/proxy/image_noise_on_proxy.jpeg", "rb")
file_chunk = file.read(2048)

while file_chunk:
    proxy_server_second.send(file_chunk)
    file_chunk = file.read(2048)

file.close()
proxy_server_second.close()
