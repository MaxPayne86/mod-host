#!/usr/bin/env python
# Description: this is a load test. We first open a connection to mod-host
# and then we try to load the same plugin a high number of times until the
# server dies. It should eats a lot of CPU also!

import socket, time
import subprocess as sp
from psutil import Process

def check_mod_host(pid):
    if sp.check_output("pgrep mod-host; exit 0", shell=True) != pid:
        print('mod-host died')
        exit(1)

def send_command(pid, s, command):
    print('sent:', command)
    s.send(str.encode(command))
    
    check_mod_host(pid)

    try:
        resp = s.recv(1024)
        if resp: print('resp:', resp)
        return True

    except Exception:
        return False

def main():
    # get mod-host pid
    pid = sp.check_output("pgrep mod-host; exit 0", shell=True)
    if pid == b'':
        print('mod-host is not running')
        exit(0)

    # setup socket
    s = socket.socket()
    s.connect(('localhost', 5555))
    s.settimeout(0.5)

    #jackdpid = sp.check_output("pgrep jackd; exit 0", shell=True)
    #p = Process(int(jackdpid))
    p = Process(int(pid))

    for i in range(25):
        send_command(pid, s, 'add http://lv2plug.in/plugins/eg-amp %i' % i)
        print("CPU:{0} RAM:{1}".format(p.cpu_percent(),p.memory_percent()))
                                          
if __name__ == "__main__": main()
