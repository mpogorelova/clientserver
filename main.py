"""
Это клиент-серверное приложение
"""

import socket
from pyparsing import Word, nums, ZeroOrMore, Optional, oneOf


# 127.0.0.1 13000 -s -t -f log_output
def parser(variable):
    """
    Это парсер, который выполняет разбор команды клиента
    """
    port_name = (Word(nums))('port_entered')
    host_name = Word(nums)
    full_host_name = (host_name + ZeroOrMore('.' + host_name))('host_entered')
    flag1 = (Optional('-s'))('mode_flag')
    flag2 = (Optional('-' + oneOf('u t')))('delivery_flag')
    flag3 = ('-' + oneOf('o f'))('log_flag')
    log_output = Optional('log_output')
    parse_module = full_host_name + port_name + flag1 + flag2 + flag3 + log_output
    res = parse_module.parseString(variable)
    host_entered = ''.join(res.host_entered)
    port_entered = res.port_entered
    mode_flag = res.mode_flag
    delivery_flag = ''.join(res.delivery_flag)
    log_flag = ''.join(res.log_flag)
    return host_entered, port_entered, mode_flag, delivery_flag, log_flag


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
            print('UDP-сокет создан')
            sock.bind((host, port))
            data = sock.recvfrom(1024)
            received = data[0]
            addr = data[1]
            info = str(addr)
            print('подсоединился:', addr)
            sock.sendto(bytes(info, encoding='UTF-8'),addr)
            sock.close()
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('TCP-сокет создан')
        sock.bind((host, port))
        print('Сервер готов слушать')
        sock.listen()
        while 1:
            conn, addr = sock.accept()
            data2 = str(addr)
            print('подсоединился:', addr)
            data = conn.recv(1024)
            print(str(data))
            conn.send(bytes(data2, encoding='UTF-8'))
            conn.close()


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
        message = input('Введите сообщение')
        sock.sendto(bytes(message, encoding='UTF-8'),(host, port))
        data = sock.recvfrom(1024)
        print(data[0])
        sock.close()
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('TCP-сокет создан')
        sock.connect((host, port))
        message = input('Введите сообщение')
        sock.send(bytes(message, encoding='UTF-8'))
        data = sock.recv(1024)
        print(data)
        sock.close()



if __name__ == '__main__':
    cmd = input()
    host_ent, port_ent, mode, delivery, log = parser(cmd)
    print(host_ent, port_ent, mode, delivery, log)
    if mode == '-s':
        server(host_ent, port_ent, delivery)
    else:
        client(host_ent, port_ent, delivery)
