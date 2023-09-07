import subprocess
import sys
import os
from configparser import ConfigParser, ExtendedInterpolation
config = ConfigParser(interpolation=ExtendedInterpolation())
config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
config.read(f'{config_path}/config.ini')
# config.read('config.ini')
terminal_emulator = config['General']['terminal']

def run_tools(command):
    try:
        command_parts = command.split(" ")
        command_parts.insert(0, terminal_emulator)
        # command_parts.insert(1, '-hold')
        command_parts.insert(1, '-e')
        process = subprocess.Popen(command_parts)
        process.wait()
    except:
        print('[-] Error Running Tool')
        sys.exit(1)

