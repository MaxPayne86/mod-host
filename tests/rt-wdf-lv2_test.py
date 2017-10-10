#!/usr/bin/env python

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
s.settimeout(0.5)

def check_mod_host():
    if sp.check_output("pgrep mod-host; exit 0", shell=True) != pid:
        print('mod-host died')
        exit(1)

def send_command(command):
    print('sent:', command)
    s.send(str.encode(command))
    check_mod_host()
    resp=""
    try:
        resp = s.recv(1024)
        print(resp)
        return True

    except Exception:
        print(resp)
        return False

plugins = [
'http://aidadsp.cc/plugins/wt-rdf_lv2/JTM45',
'http://aidadsp.cc/plugins/wt-rdf_lv2/ToneStack'
]

for i, plugin in enumerate(plugins):
    send_command('add %s %i' % (plugin, i))

time.sleep(2.5)

for i in range(len(plugins)):
    send_command('remove %i' % i)
