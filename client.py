import logging
import json
import socket

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

address_to_server = ('::1', 36666)


def validate_message(response):
    error = response.get('payload').get('error_message')

    if error:
        logger.info('Получил такую ошибку  %s', error)


# long_text = 'BOBR KURWA I PERDOLEL' * 150


def crate_body_message() -> dict:
    message_type = input('Enter message type to send: ')
    data = input('Enter data to send: ')
    long_end_approve = input('Send long text?')
    long_start_approve= input('Yes?')

    my_data = {
        'type': message_type,
        'payload': {
            'text': data,
        }
    }
    message = f'START_MESSAGE{my_data}END_MESSAGE'
    if long_end_approve:
        message = message + ('END_MESSAGE' * 100)
    if long_start_approve:
        message = 'START_MESSAGE' + 'XEXE_PIDR_XEXE' + ('START_MESSAGE'*99) + message
    return message


# def clinet_back_client():
    # try:
    #     message = crate_body_message()
    # except KeyboardInterrupt:
    #     logger.info('Вы закрыли клиент. Хорошо дня')
    #     return
    #
    # logger.info('Send message "%s" to server', message)
    # s.send(json.dumps(message).encode())
    # s.send(json.dumps(message).encode())
    #
    # try:
    #     response = s.recv(1024)
    #     logger.info('Get response "%s" from server', message)
    # except KeyboardInterrupt:
    #     return
    #
    # if not response:
    #     logger.info('ДУДОС УДАЛАСЯ. СЕРВЕР ПАЛ. МИР ФРОНТЕНДА ПОБЕДИЛ')
    #     return
    #
    # response = json.loads(response)
    # logger.info('Считал такое сообщение с сервера = %s', response)
    # validate_message(response)


def client():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
        for i in range(5):
            s.connect(address_to_server)
        while True:
            try:
                message = crate_body_message()
            except KeyboardInterrupt:
                logger.info('Вы закрыли клиент. Хорошо дня')
                break
            logger.info('Send message "%s" to server', message)
            s.send(json.dumps(message).encode())
            s.sendall(json.dumps(message).encode())
            try:
                response = s.recv(1024)
                logger.info('Get response "%s" from server', message)
            except KeyboardInterrupt:
                break

            if not response:
                logger.info('ДУДОС УДАЛАСЯ. СЕРВЕР ПАЛ. МИР ФРОНТЕНДА ПОБЕДИЛ')
                break

            response = json.loads(response)
            logger.info('Считал такое сообщение с сервера = %s', response)
            validate_message(response)



if __name__ == '__main__':
    try:
        client()
    except Exception:
        exit(1)

