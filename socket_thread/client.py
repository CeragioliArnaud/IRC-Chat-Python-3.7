import socket

hote = "localhost"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(port))

my_bytes = bytearray()
my_bytes.append(123)
my_bytes.append(125)

socket.send(my_bytes)

print("Close")
socket.close()