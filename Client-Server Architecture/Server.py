import os.path
from socket import *

import cv2
import logging

logging.basicConfig(
    filename="logs/server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

server = socket(AF_INET, SOCK_STREAM)
server.bind(("localhost", 8080))
server.listen(10)
logging.info("Ожидание подключения...")


def chunk(file_name):
    file = open(file_name, "wb")
    file_chunk = client_socket.recv(2048)
    while file_chunk:
        file.write(file_chunk)
        file_chunk = client_socket.recv(2048)
        if not file_chunk:
            break
    file.close()


client_socket, client_address = server.accept()
chunk("image/server/image_noise_on_proxy.jpeg")
logging.info("Все изображения были успешно получены...")
noise_image = cv2.imread("image/server/image_noise_on_proxy.jpeg")
print(f"Размер поврежденного изображения: {os.path.getsize('image/server/image_noise_on_proxy.jpeg')}")
logging.info("Идет процесс восстановления изображения...")
denoise_image = cv2.medianBlur(noise_image, 5)
cv2.imwrite("image/server/denoise_image_on_server.jpeg", denoise_image)
logging.info("Изображение было успешно восстановленно")
print(f"Размер восстановленного изображения: {os.path.getsize('image/server/denoise_image_on_server.jpeg')}")
client_socket.close()
server.close()