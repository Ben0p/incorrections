#! /usr/bin/python3.6
import sys
import socket
import time
from multiprocessing import Pool
import curses
from datetime import datetime, timedelta
import subprocess
import re

##################################################################
# If you are reading this than what are you doing with your life #
# Made with coffee by Ben0 over several night shifts             #
# Don't judge the code, it was rushed ok                         #
# about 5 lines to do the job, 265 to print bullshit to terminal #
##################################################################

dest_ip_list = []
source_ip = '10.20.23.230'
source_port = 5019
binding_ip = '10.20.64.253'
dest_port = 5019
ip_list = '/home/minesys/Desktop/final.conf'

transmit_ok = 0
transmit_errors = 0
transmit_perc = 0
receive_ok = 0
receive_errors = 0
receive_perc = 0
send_ok = 0
send_errors = 0
send_perc = 0

_uptime = ''
timestamp = time.time()
delay = 0
prev_delay = 0

netstat = ''


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
        return(ip, True)
    except:
        return(ip, False)
    s.shutdown(s.SHUT_RDWR)
    s.close()

def uptime(seconds):
    intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
    )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(int(value), name))
    return(', '.join(result[:4]))

def getBuffer():
    out = subprocess.Popen(['netstat', '-a'], stdout=subprocess.PIPE)
    stdout,stderr = out.communicate()
    decoded = stdout.decode("utf-8").split('\n')
    for line in decoded:
        if 'localhost.localdom:5019' in line:
            splitline = line.split()
            return(splitline)



class display():

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, -1)
        self.ascii_art = asciiArt()


    def screen(self):
        self.stdscr.clear()

        self.stdscr.border(0)

        self.stdscr.addstr(0,32,"Minesystems' UDP Relay")

        self.box1 = curses.newwin(3, 28, 1, 29)
        self.box2 = curses.newwin(5, 28, 4, 1)
        self.box3 = curses.newwin(5, 28, 4, 29)
        self.box4 = curses.newwin(5, 28, 4, 57)
        self.box5 = curses.newwin(4, 28, 9, 1)
        self.box6 = curses.newwin(4, 28, 9, 29)
        self.box7 = curses.newwin(4, 28, 9, 57)
        self.box8 = curses.newwin(3, 28, 1, 1) #Top Left
        self.box9 = curses.newwin(3, 28, 1, 57) #Top Right
        self.box10 = curses.newwin(20, 44, 13, 20)

        self.box1.box()
        self.box2.box()
        self.box3.box()
        self.box4.box()
        self.box5.box()
        self.box6.box()
        self.box7.box()
        self.box8.box()
        self.box9.box()
        self.box10.box()


        self.box1.addstr(0,11,"Uptime")
        self.box2.addstr(0,6,"Corrections In")
        self.box3.addstr(0,6,"Corrections Out")
        self.box4.addstr(0,5,"Corrections Sent")
        self.box5.addstr(0,12,"List")
        self.box6.addstr(0,10,"Binding")
        self.box7.addstr(0,11,"Buffer")
        self.box8.addstr(0,10,"Warning")
        self.box9.addstr(0,12,"Delay")
        self.box10.addstr(0,17,"A Satellite")

        self.box1.addstr(1,1,' '*26)
        self.box1.addstr(1,1,_uptime.center(26, ' '))

        self.box2.addstr(1,1,'      OK: {}'.format(receive_ok))
        self.box2.addstr(2,1,'    Fail: {}'.format(receive_errors))
        self.box2.addstr(3,1,' Percent: {}%'.format(receive_perc))

        self.box3.addstr(1,1,'      OK: {}'.format(transmit_ok))
        self.box3.addstr(2,1,'    Fail: {}'.format(transmit_errors))
        self.box3.addstr(3,1,' Percent: {}%'.format(transmit_perc))

        self.box4.addstr(1,1,'      OK: {}'.format(send_ok))
        self.box4.addstr(2,1,'    Fail: {}'.format(send_errors))
        self.box4.addstr(3,1,' Percent: {}%'.format(send_perc))

        self.box5.addstr(1,1,'    File: final.conf')
        self.box5.addstr(2,1,'     IPs: {}'.format(len(dest_ip_list)))

        self.box6.addstr(1,1,'  Local:{}:{}'.format(binding_ip, dest_port))
        self.box6.addstr(2,1,' Remote:{}:{}'.format(source_ip, source_port))

        self.box7.addstr(1,1,'  Rx: {} kb'.format(round(int(netstat[1])/1000)))
        self.box7.addstr(2,1,'  Tx: {} kb'.format(round(int(netstat[2])/1000)))

        self.box8.addstr(1,1,' '*26)
        self.box8.addstr(1,1,'DO NOT CLOSE'.center(26, ' '), curses.color_pair(1))

        self.box9.addstr(1,1,' '*26)
        self.box9.addstr(1,1,str(delay).center(26, ' '))

        for y, line in enumerate(self.ascii_art.splitlines(), 2):
            self.box10.addstr(y, 2, line)
        
        self.stdscr.refresh()
        self.box1.refresh()
        self.box2.refresh()
        self.box3.refresh()
        self.box4.refresh()
        self.box5.refresh()
        self.box6.refresh()
        self.box7.refresh()
        self.box8.refresh()
        self.box9.refresh()
        self.box10.refresh()

def asciiArt():
    return(
    r'''
                }--O--{
                  [^]
                 /ooo\
 ______________:/o   o\:______________
|=|=|=|=|=|=|:A|":|||:"|A:|=|=|=|=|=|=|
^""""""""""""""!::{o}::!""""""""""""""^
                \     /
                 \.../
      ____       "---"       ____
     |\/\/|=======|*|=======|\/\/|
     :----"       /-\       "----:
                 /ooo\
                #|ooo|#
                 \___/
    '''
    )



if __name__ == '__main__':
    ipList()
    how_many = len(ip_list)

    p = Pool(processes=how_many)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)
    s.bind((binding_ip, source_port))

    _display = display()

    while True:
        try:
            s.settimeout(None)
            data, addr = s.recvfrom(32768)
            receive_ok += 1
        except:
            receive_errors += 1
            continue

        try:
            if addr[0] == source_ip:
                prev_delay = time.time()
                transmit_ok += 1
                results = [p.apply_async(send, args=(ip, data, s,)) for ip in dest_ip_list]
                output = [p.get() for p in results]
                for i in output:
                    if i[1] == True:
                        send_ok += 1
                    else:
                        send_errors += 1

        except:
            transmit_errors += 1

        
        uptime_seconds = time.time()-timestamp
        _uptime = uptime(uptime_seconds)

        try:
            receive_perc = round((1-(receive_errors/receive_ok))*100, 2)
        except:
            receive_perc = 100
        try:
            transmit_perc = round((1-(transmit_errors/transmit_ok))*100, 2)
        except:
            transmit_perc = 100
        try:
            send_perc = round((1-(send_errors/send_ok))*100, 2)
        except:
            send_perc = 100
        
        netstat = getBuffer()
        delay = time.time()-prev_delay

        _display.screen()
