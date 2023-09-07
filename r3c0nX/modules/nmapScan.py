import subprocess
import re
import sys
import threading
import time
import os
from configparser import ConfigParser, ExtendedInterpolation
config = ConfigParser(interpolation=ExtendedInterpolation())
config_path = os.path.join(os.path.dirname(__file__), '..', 'config')

config.read(f'{config_path}/config.ini')
# config.read('config.ini')
# print(config_path)
terminal_emulator = config['General']['terminal']
config.read(f'{config_path}/nmapscripts.ini')

def advanced_scan(port, service, path, machine, ip):
    try:
        port = port.strip()
        print(f'[+] Running NMAP Scan on port {port} with service {service}\n\n')
        script = config['SCRIPT'][service]
        Scan = subprocess.Popen([terminal_emulator, '-e', 'nmap', '-vv', '-p' + port, '--script', script, '-oN', path + '/' + machine + '/enumeration/' + port + '.nmap', ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = Scan.communicate()
        # print('[+] Scan Complete on port ' + port + '\n\n')
    except:
        print('[-] Error Running NMAP Scan')
        sys.exit(1)

def nmap_scan(path, machine, ip):
    try:
        print('[+] Running NMAP Scan')
        nmap = subprocess.Popen(['nmap', '-vv', '-oX', path + '/' + machine + '/enumeration/nmap.xml', ip], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(nmap.stdout.readline, b''):
            print(line.rstrip().decode('utf-8'))
    except:
        print('[-] Error Running NMAP Scan')
        sys.exit(1)

    
