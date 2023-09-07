from configparser import ConfigParser, ExtendedInterpolation
import os
# from r3c0nX.config import *
def update_config(ip, path, machine_name):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config')

    for file in os.listdir(config_path):
        if file.endswith('.ini'):
            #print(f'[*] Updating {file}')
            config = ConfigParser(interpolation=ExtendedInterpolation())
            config.read(f"{config_path}/{file}")
            config['General']['IP'] = ip
            config['General']['Path'] = path
            config['General']['machine'] = machine_name
            with open(f"{config_path}/{file}", 'w') as configfile:
                config.write(configfile)
            #print(f'[+] Updated {file}')
