import sys
import socket
import time
import threading


dest_ip_list = []
source_ip = '10.20.23.230'
source_port = 5019
binding_ip = '10.20.64.253'
dest_port = 5019
ip_list = 'final.conf'

with open(ip_list, 'r') as f:
    for line in f.readlines():
        if line[0] == '#':
            continue
        else:
            stripped_line = line.strip('\n')
            split_line = stripped_line.split(':')
            dest_ip = split_line[1].split('/')[0]
            dest_ip_list.append(dest_ip)



def bind():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((binding_ip, source_port))
    except:
	    print('Failed to bind on port ' + str(source_port))

    print('Listening to: {}:{}'.format(source_ip, source_port))
    while True:
        try:
            s.settimeout(1.1)
            data, addr = s.recvfrom(32768)
        except socket.timeout:
            print('Timed out')
            continue

        if addr[0] == source_ip:
            print(time.time())
            for ip in dest_ip_list:
                try:
                    s.settimeout(0.0001)
                    s.sendto(data, (ip, dest_port))
                except socket.timeout:
                    print('{} timed out'.format(ip))
                    continue

bind()
