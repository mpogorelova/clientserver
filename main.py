"""
Это клиент-серверное приложение
"""
import logging
import socket
from pyparsing import Word, nums, ZeroOrMore, Optional, oneOf, printables


# 127.0.0.1 13000 -s -t -f log_output
def parser(variable):
    """
    Это парсер, который выполняет разбор команды клиента
    """
    port_name = (Word(nums))('port_entered')
    full_host_name = ((Word(nums)) + ZeroOrMore('.' + (Word(nums))))('host_entered')
    flag1 = (Optional('-s'))('mode_flag')
    flag2 = (Optional('-' + oneOf('u t')))('delivery_flag')
    flag3 = (Optional('-' + oneOf('o f'))('log_flag'))
    log_output = (Optional(Word(printables)))('file_name')
    parse_module = full_host_name + port_name + flag1 + flag2 + flag3 + log_output
    res = parse_module.parseString(variable)
    host_entered = ''.join(res.host_entered)
    port_entered = res.port_entered
    mode_flag = res.mode_flag
    delivery_flag = ''.join(res.delivery_flag)
    log_flag = ''.join(res.log_flag)
    file_name = res.file_name
    return host_entered, port_entered, mode_flag, delivery_flag, log_flag, file_name


def server(host_var, port_var, deliv):
    """
    Это серверная часть приложения
    """
    host = host_var
    port = int(port_var)
    tcp_or_udp = deliv
    if tcp_or_udp == '-u':
        while 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logging.info('UDP-сокет создан')
            sock.bind((host, port))
            data = sock.recvfrom(1024)
            addr = data[1]
            logging.info('Сообщение получено')
            info = str(addr)
            print('подсоединился:', addr)
            sock.sendto(bytes(info, encoding='UTF-8'), addr)
            logging.info('Сообщение отправлено')
            sock.close()
            logging.info('Сокет закрыт')
            break
            # прерывание для тестирования, т.к. по заданию сервер слушает в бесконечном цикле
    else:
        while 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.info('TCP-сокет создан')
            sock.bind((host, port))
            logging.info('Сервер готов слушать')
            sock.listen()
            conn, addr = sock.accept()
            data2 = str(addr)
            logging.info('Сообщение получено')
            print('подсоединился:', addr)
            data = conn.recv(1024)
            print(str(data))
            conn.send(bytes(data2, encoding='UTF-8'))
            logging.info('Сообщение отправлено')
            conn.close()
            logging.info('Сокет закрыт')
            break
            # прерывание для тестирования, т.к. по заданию сервер слушает в бесконечном цикле


def client(host_var, port_var, deliv):
    """
    Это клиентская часть приложения
    """
    host = host_var
    port = int(port_var)
    tcp_or_udp = deliv
    if tcp_or_udp == '-u':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('UDP-сокет создан')
        message = input('Введите сообщение\n')
        sock.sendto(bytes(message, encoding='UTF-8'), (host, port))
        data = sock.recvfrom(1024)
        print(data[0])
        sock.close()
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('TCP-сокет создан')
        sock.connect((host, port))
        message = input('Введите сообщение\n')
        sock.send(bytes(message, encoding='UTF-8'))
        data = sock.recv(1024)
        print(data)
        sock.close()


def logger(log_type, name):
    """
    Это функция-логгер
    """
    if log_type == '-f':
        logging.basicConfig(level=logging.INFO, filename=name)
    else:
        logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    cmd = input('Enter cmd like: <host> <port> [-s] [-t | -u] [-o | -f <file>]\n')
    host_ent, port_ent, mode, delivery, log, title = parser(cmd)
    logger(log, title)
    if mode == '-s':
        server(host_ent, port_ent, delivery)
    else:
        client(host_ent, port_ent, delivery)
