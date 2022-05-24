# socket module import!
import socket

# socket create and connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("141.223.140.3", 8888))

# send msg
test_msg = "안녕하세요 상대방님"
sock.send(test_msg)

# recv data
data_size = 512
data = sock.recv(data_size)

# connection close
sock.close()