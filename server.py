import socket


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(10)
    print('Server run')
    try:
        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
    except KeyboardInterrupt:
        return

    while True:
        data = client_socket.recv(1024)
        print(str(data.decode('utf-8')))
        client_socket.send(b'Ok')


if __name__ == '__main__':
    server()
