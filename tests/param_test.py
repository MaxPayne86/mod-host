#!/usr/bin/env python
# Description: in this test we load an lv2 plugin to mod-host
# and we change slowly one parameter so the result should be audible

import socket, time
import subprocess as sp

# get mod-host pid
pid = sp.check_output("pgrep mod-host; exit 0", shell=True)
if pid == b'':
    print('mod-host is not running')
    exit(0)

# setup socket
s = socket.socket()
s.connect(('localhost', 5555))
s.settimeout(5)

def check_mod_host():
    if sp.check_output("pgrep mod-host; exit 0", shell=True) != pid:
        print('mod-host died')
        exit(1)

def send_command(command):
    print('sent:', command)
    s.send(str.encode(command))
    
    check_mod_host()

    try:
        resp = s.recv(1024)
        if resp: print('resp:', resp)
        return True

    except Exception:
        return False

send_command('add http://lv2plug.in/plugins/eg-amp 0')

value_min = -90.0
value_max = 24.0
value = value_min
steps = 5
inc = (value_max - value_min) / steps

for i in range(steps):
    value += inc
    send_command('param_set 0 gain %f' % value)
    send_command('param_get 0 gain')

send_command('remove 0')
