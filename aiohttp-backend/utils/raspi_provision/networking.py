import asyncio

import re

import subprocess
import os

"""
Simple module for controlling wifi and access point mode on raspberru pi.
MUST be run as root.
Does NOT do error handling.
"""


RASPI_PROV_PATH = os.environ.get('RASPI_PROV')
if not RASPI_PROV_PATH:
    raise RuntimeError('No "RASPI_PROV" environment variable detected.')

def set_wifi(ssid, passwd):
    with open(f'{RASPI_PROV_PATH}/config_files/wpa_supplicant.conf.template') as i, \
         open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as o:
             template = i.readlines()
             template[-3] = template[-3].replace('SSID', ssid)
             template[-2] = template[-2].replace('PASSWORD', passwd)
             o.writelines(template)
    return True

def get_current_wifi():
    with open('/etc/wpa_supplicant/wpa_supplicant.conf') as f:
         conf = f.readlines()
         ssid = re.search('"(.+)"\\n', conf[-3]).group(1)
         passwd = re.search('"(.+)"\\n', conf[-2]).group(1)
    return ssid, passwd

def get_current_ip(interface='wlan0'):
    result = subprocess.check_output(['/sbin/ifconfig', f'{interface}'], universal_newlines=True)
    try:
        inet = [line for line in result.splitlines() if 'inet ' in line][0]
    except IndexError:
        raise ValueError(f'No valid ip address assigned to interface: {interface}.')
    ip = inet.split()[1]
    if re.match('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', ip):
        return ip
    else:
        raise ValueError(f'No valid ip address assigned to interface: {interface}.')

async def switch_AP_mode(active=True):
    state = 'enabled' if active else 'disabled'
    processes = []
    if active:
        processes.append(asyncio.create_subprocess_exec(*['cp', f'{RASPI_PROV_PATH}/config_files/dhcpcd.conf.enable', '/etc/dhcpcd.conf']))
        processes.append(asyncio.create_subprocess_exec(*['/bin/systemctl', 'enable', 'hostapd']))
        processes.append(asyncio.create_subprocess_exec(*['/bin/systemctl', 'start', 'hostapd']))
        #result = subprocess.check_output(['cp', f'{RASPI_PROV_PATH}/config_files/dhcpcd.conf.enable', '/etc/dhcpcd.conf'])
        #result = subprocess.check_output(['/bin/systemctl', 'enable', 'hostapd'])
        #result = subprocess.check_output(['/bin/systemctl', 'start', 'hostapd'])
    else:
        processes.append(asyncio.create_subprocess_exec(*['cp', f'{RASPI_PROV_PATH}/config_files/dhcpcd.conf.disable', '/etc/dhcpcd.conf']))
        processes.append(asyncio.create_subprocess_exec(*['/bin/systemctl', 'start', 'hostapd']))
        processes.append(asyncio.create_subprocess_exec(*['/bin/systemctl', 'disable', 'hostapd']))
        #result = subprocess.check_output(['cp', f'{RASPI_PROV_PATH}/config_files/dhcpcd.conf.disable', '/etc/dhcpcd.conf'])
        #result = subprocess.check_output(['/bin/systemctl', 'stop', 'hostapd'])
        #result = subprocess.check_output(['/bin/systemctl', 'disable', 'hostapd'])
    for proc in processes:
        await proc
    return True

def reboot():
    subprocess.check_output(['reboot'])

