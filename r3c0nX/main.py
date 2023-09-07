import os
import sys
import subprocess
import re
import argparse
import threading
import time
from r3c0nX.modules import createFolders, nmapScan, runTools,filterResult, updateConfig
from r3c0nX.config import *
from configparser import ConfigParser, ExtendedInterpolation
import json
config = ConfigParser(interpolation=ExtendedInterpolation())
wellknownservices = ConfigParser(interpolation=ExtendedInterpolation())

class Color:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    

banner = """
=======================================================
=       ======   =============      ==========   ==   =
=  ====  ===   =   ==========   ==   ==========  ==  ==
=  ====  ==   ===   =========  ====  ==========  ==  ==
=  ===   =======   ====   ===  ====  ==  = =====    ===
=      =======    ====  =  ==  ====  ==     =====  ====
=  ====  =======   ===  =====  ====  ==  =  ====    ===
=  ====  ==   ===   ==  =====  ====  ==  =  ===  ==  ==
=  ====  ===   =   ===  =  ==   ==   ==  =  ===  ==  ==
=  ====  =====   ======   ====      ===  =  ==  ====  =
=======================================================
    -D2Cy 
"""

print(f"{Color.GREEN}{banner}{Color.CYAN}")

argparser = argparse.ArgumentParser()
argparser.add_argument('-p', '--path', help='Path to Create Folders')
argparser.add_argument('-m', '--machine', help='Machine Name/IP')
argparser.add_argument('-i', '--ip', help='Machine IP')

terminal_emulator = "xterm"

args = argparser.parse_args()
if len(sys.argv) < 4:
    print(f'{Color.RED}[-] Not Enough Arguments Passed')
    argparser.print_help()
    sys.exit(1)

config_path = os.path.join(os.path.dirname(__file__) , 'config')
config.read(f'{config_path}/config.ini')
wellknownservices.read(f'{config_path}/wellknownservices.ini')
#Global Variables
threads = []
open_ports = []

#Verify Path
if not os.path.exists(args.path):
    print(f'{Color.RED}[-] Path Does Not Exist{Color.RESET}')
    sys.exit(1)
absolute_path = os.path.abspath(args.path)



def scriptScan():
    for line in open(absolute_path + '/' + args.machine + '/others/service.log', 'r'):
        service,port = line.split('\t')
        thread = threading.Thread(target=nmapScan.advanced_scan, args=(port, service, absolute_path, args.machine, args.ip,))
        threads.append(thread)
        thread.start()
        time.sleep(2)


def runToolHelper(service,port):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(f"{config_path}/{service}.ini")
        print(f'\n\n{Color.YELLOW}List of Available Tools for {service}{Color.RESET}\n')
        tools = config['Tools']
        for tool in tools:
            print(tool+". "+config.get('Tools', tool))
        print(f'\n\n{Color.MAGENTA}[+] Enter Tools to Run on Port  {port} {Color.GREEN} (Ex: 1,2 ) (Enter 0 to exit) :', end='')
        tools = input()
        if tools == '0':
            return
        
        for tool in tools.split(','):
            tool = tool.strip()
            cmd = config.get('Tools', tool)
            try:
                thread = threading.Thread(target=runTools.run_tools, args=(cmd,))
                threads.append(thread)
                thread.start()
                time.sleep(2)
            except:
                print(f'{Color.RED}[-] Invalid Tool{Color.RESET}')


def runWellKnownTools():
    file = open(absolute_path + '/' + args.machine + '/others/service.log', 'r')
    for line in file:
        service,ports = line.split('\t')
        # print(ports)
        if service == 'smb':
            ports = ports.strip()
            runToolHelper(service,ports)
        else:
            for port in ports.split(','):
                port = port.strip()
                config = ConfigParser(interpolation=ExtendedInterpolation())
                try:
                    config.read(f"{config_path}/{service}.ini")
                    config['General']['port'] = port
                    with open(f"{config_path}/{service}.ini", 'w') as configfile:
                        config.write(configfile)
                    runToolHelper(service,port)
                except:
                    print(f'{Color.RED}[-] Config File Not Found{Color.RESET}')

def displayFFUFOutput(file):
    with open(file) as ffuf_log:
        data = json.load(ffuf_log)
    results = data.get('results', [])
    # Filter URLs with a status code of 200
    status_200_urls = [result['url'] for result in results if result.get('status') == 200]
    status_30x_urls = [result['url'] for result in results if result.get('status') >= 300 or result.get('status') < 400]
    # status_40x_urls = [result['url'] for result in results if result.get('status') >= 400 or result.get('status') < 500]
    # Print the filtered URLs
    print(f'{Color.YELLOW}{"-"*100}{Color.RESET}')

    print(f'{Color.MAGENTA}[*] 20x URLs {Color.RESET}')
    for url in status_200_urls:
        print(url)
                
    print(f'{Color.YELLOW}{"-"*100}{Color.RESET}')
    print(f'{Color.MAGENTA}[*] 30x URLs {Color.RESET}')
    for url in status_30x_urls:
        print(url)
                
    print(f'{Color.YELLOW}{"-"*100}{Color.RESET}')
    # print(f'{Color.MAGENTA}[*] 40x URLs {Color.RESET}')
    # for url in status_40x_urls:
    #     print(url)
                
    print(f'{Color.GREEN}{"-"*100}{Color.RESET}')


def displayOutput():
    logs = open(absolute_path + '/' + args.machine + '/others/service.log', 'r')
    
    for file in os.listdir(absolute_path + '/' + args.machine + '/enumeration'):
        try:
            if file.endswith('.nmap'):
                print(f'{Color.CYAN}[*] NMAP Output for Port/Ports {(file.split(".")[0])}{Color.RESET}')
                print(f'{Color.GREEN}{"-"*100}{Color.RESET}')
                with open(absolute_path + '/' + args.machine + '/enumeration/' + file, 'rb') as nmap_log:
                    for line in nmap_log:
                        print(line.decode('utf-8').strip())
                print(f'{Color.GREEN}{"-"*100}{Color.RESET}')

            if file.endswith('.ffuf'):
                print(f'{Color.CYAN}[*] FFUF Output: Port {(file.split(".")[0]).split("_")[2]}{Color.RESET}')
                print(f'{Color.GREEN}{"-"*100}{Color.RESET}')
                displayFFUFOutput(absolute_path + '/' + args.machine + '/enumeration/' + file)
                print(f'{Color.GREEN}{"-"*100}{Color.RESET}')

            if file.endswith('.ftp'):
                print(f'{Color.CYAN}[*] FTP Output:{Color.RESET}')
                print(f'{Color.GREEN}{"-"*100}{Color.RESET}')
                with open(absolute_path + '/' + args.machine + '/enumeration/' + file, 'rb') as ftp_log:
                    for line in ftp_log:
                        print(line.decode('utf-8').strip())
                print(f'{Color.GREEN}{"-"*100}{Color.RESET}')
        except:
            print(f'{Color.RED}[-] Error Reading File: {file}{Color.RESET}')
            

def main():
    updateConfig.update_config(args.ip, absolute_path, args.machine) # Update Config Files
    createFolders.create_folders(path=absolute_path, machine=args.machine)  # Create Folders
    print(f'{Color.CYAN}[+] Running NMAP Scan\n\n{Color.RESET}') 
    nmapScan.nmap_scan(path=absolute_path, machine=args.machine, ip=args.ip) # Run NMAP Scan
    print(f'{Color.CYAN}[+] Filtering Well Known Ports\n\n ')
    filterResult.filter_well_known_ports(path=absolute_path, machine=args.machine) # Filter Well Known Ports and Run NMAP Scripts
    print(f'{Color.CYAN}[+] Running NMAP Scripts\n\n')
    scriptScan()
    print(f'{Color.CYAN}[+] Running Tools on Well Known Services\n\n') 
    runWellKnownTools()

                
    for thread in threads:
        thread.join()
    print(f'\n\n\n{Color.CYAN}[+] Basic Enumeration Complete{Color.RESET}\n\n\n')

    print(f"Output of Tools :")
    displayOutput()

    

    





# if __name__ == '__main__':
#     main()







