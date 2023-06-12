import json
import socket
from random import randint
from time import sleep
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

class Error(Exception):
    pass
def decode(data) -> dict:
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        chunks = []
        data = data.decode()
        chunks.append(data)

    logger.info(data)

    if not data:
        raise Error('Error: data is empty')

    if 'START_MESSAGE' not in data or 'END_MESSAGE' not in data:
        raise Error('Error: data invalid message')

    data = data.replice('START_MESSAGE', '').replace('END_MESSAGE', '')

    try:
        data = dict(data)
    except ValueError:
        raise Error('Error: data is not dict')

    if len(data) != 2:
        raise Error('Error: data is many keys')

    if 'type' not in data or 'payload' not in data:
        raise Error('Error: type or payload is not defined')

    if data['type'] != "message":
        raise Error('Error: type is not message')

    if not isinstance(data['payload'], dict):
        raise Error('Error: payload is not dict')

    return data


def server():
    addr = ("", 36666)
    if socket.has_dualstack_ipv6():
        server_socket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        server_socket = socket.create_server(addr)

    server_socket.listen(10)

    logger.info('Server run')
    while True:
        try:
            client_socket, addr = server_socket.accept()
            logger.info(f'Connection from  {addr}')
        except KeyboardInterrupt:
            return

        while True:
            try:
                data = client_socket.recv(1024)
            except ConnectionResetError:
                logger.info(f'Connection closed {addr}')
                break
            except KeyboardInterrupt:
                logger.info(f'Connection closed {addr}')
                return

            error_message = None
            try:
                data = decode(data)
            except Error as e:
                error_message = 'START_MESSAGE\n' + str(e) + 'END_MESSAGE\n'

            logger.info(data)

            message = {"type": "system", "payload": {"received": True}}
            if error_message:
                message = {"type": "system", "payload": {"error_message": error_message}}

            try:
                logger.info(f'Send:{message}')
                # sleep(randint(0, 10))
                client_socket.send(json.dumps(message).encode('utf-8') + b'\n')
            except BrokenPipeError:
                logger.info(f'Connection closed, {addr}')
                break


if __name__ == '__main__':
    try:
        server()
    except Exception:
        exit(1)