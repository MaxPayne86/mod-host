#!/usr/bin/env python
# Description: in this test we scan all the plugin available
# and we try to load them on mod-host one-by-one. This takes time!

import socket, time
import subprocess as sp

# get mod-host pid
pid = sp.check_output("pgrep mod-host; exit 0", shell=True)
if pid == b'':
    print('mod-host is not running')
    exit(0)

def check_mod_host():
    if sp.check_output("pgrep mod-host; exit 0", shell=True) != pid:
        print('mod-host died')
        exit(1)

# setup socket
s = socket.socket()
s.connect(('localhost', 5555))
s.settimeout(5)

def send_command(command):
    print('sent:', command)
    s.send(str.encode(command))

    try:
        resp = s.recv(1024)
        print(resp)
        return True

    except Exception:
        return False


# get plugins list
plugins = sp.check_output('lv2ls',universal_newlines=True).split('\n');
print(plugins)

# add and remove the effects
for i, plugin in enumerate(plugins):
    if plugin != '':
        send_command('add %s %i' % (plugin, i))
        time.sleep(0.25)
        check_mod_host()
        time.sleep(0.25)
        send_command('remove %i' % i)
