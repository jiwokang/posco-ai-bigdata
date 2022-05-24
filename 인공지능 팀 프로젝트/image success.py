import socket
import cv2
from time import sleep

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('141.223.140.3', 8888))  # 127.0.0.1
server.listen()

client_socket, client_address = server.accept()

file = open('umbr.jpg', "wb")
image_chunk = client_socket.recv(2048)  # stream-based protocol

while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)

#    sleep(3)

    #내가 추가한 코드
#    unchange = cv2.imread('/home/piai/umbr.jpg',cv2.IMREAD_COLOR)
#    cv2.imshow('Unchange',unchange)
#    cv2.waitKey(5000)
#    cv2.destroyAllWindows()

file.close()
client_socket.close()  