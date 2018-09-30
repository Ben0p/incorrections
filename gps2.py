import sys
import socket
import time
from multiprocessing import Pool

dest_ip_list = []
source_ip = '10.20.23.230'
source_port = 5019
binding_ip = '10.20.64.253'
dest_port = 5019
ip_list = 'final.conf'


def ipList():
    with open(ip_list, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue
            else:
                stripped_line = line.strip('\n')
                split_line = stripped_line.split(':')
                dest_ip = split_line[1].split('/')[0]
                dest_ip_list.append(dest_ip)


def send(ip, data, s):
    try:
        s.settimeout(0.01)
        s.sendto(data, (ip, dest_port))
        print('Sent to {}'.format(ip))
    except:
        print('Failed to send to {}'.format(ip))
    s.shutdown(s.SHUT_RDWR)
    s.close()






if __name__ == '__main__':
    ipList()
    how_many = len(ip_list)
    p = Pool(processes=how_many)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)
    s.bind((binding_ip, source_port))

    while True:
        try:
            s.settimeout(None)
            data, addr = s.recvfrom(32768)
        except:
            continue
        try:
            if addr[0] == source_ip:
                print('Received from {}'.format(source_ip))
                results = [p.apply_async(send, args=(ip, data, s,)) for ip in dest_ip_list]
                output = [p.get() for p in results]
        except:
            print('Failed')
