import sys
import socket


dest_ip_list = []
source_port = 5019
dest_port = 5019
ip_list = 'final.conf'

with open(ip_list, 'r') as f:
    for line in f.readlines():
        if line[0] == '#':
            continue
        else:
            stripped_line = line.strip('\n')
            split_line = stripped_line.split(':')
            source_ip = split_line[0]
            dest_ip = split_line[1].split('/')[0]
            dest_ip_list.append(dest_ip)


def bind():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', source_port))
    except:
	    print('Failed to bind on port ' + str(source_port))

    print('Running...')
    while True:
        data, addr = s.recvfrom(32768)
        if addr == source_ip:
            for ip in dest_ip_list:
                s.sendto(data, (ip, dest_port))

bind()