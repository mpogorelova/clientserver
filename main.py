# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import logging
import socket
import sys


def client(host_client, port_client, flag_server, log):
    if flag_server in "-t":
        sock_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_c.connect((host_client, port_client))
        message = input('Введите сообщение')
        sock_c.send(bytes(message, encoding='UTF-8'))
        data = sock_c.recv(1024)
        print(data)
        sock_c.close()


def server(host_server, port_server, flag_server, log):
    if flag_server in "-u":
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log.info("Socket open UDP")
        except UnboundLocalError:
            log.error("UnboundLocalError: ")
            sys.exit(1)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        log.info("Socket open TCP")
    sock.bind((host_server, port_server))
    logging.info("Server get host and port")
    sock.listen()
    while 1:
        conn, addr = sock.accept()
        data2 = str(addr)
        print('подсоединился:', addr)
        data = conn.recv(1024)
        print(str(data))
        conn.send(bytes(data2, encoding='UTF-8'))
        logging.info("Message send")
        conn.close()
        logging.info("Socket close")


def parser(string_parser):
    host_parser = string_parser.split(' ')[0]
    port_parser = string_parser.split(' ')[1]
    flag_parser = string_parser.split(' ').copy()
    return host_parser, port_parser, flag_parser


def get_logger(flags_log):
    if flags_log in "-f":
        log = logging.getLogger()
        fh = logging.FileHandler(flags_log[-1], encoding='utf-8')
        log.addHandler(fh)
    else:
        log = logging.getLogger()
        sh = logging.StreamHandler(stream=sys.stdout)
        log.addHandler(sh)
    return log


# Press the green button in the gutter to run the script.
# <host> <port> [-s] [-t | -u] [-o | -f <file>]
if __name__ == '__main__':
    input_string = input()
    host, port, flags = parser(input_string)
    logger = get_logger(flags)
    if flags in "-s":
        server(host, port, flags, logger)
    else:
        client(host, port, flags, logger)
