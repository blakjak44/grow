import subprocess
import os
import re

"""
Simple module for controlling wifi and access point mode on raspberru pi.
MUST be run as root.
Does NOT do error handling.
"""

RASPI_PROV_PATH = os.environ.get('RASPI_PROV')
if not RASPI_PROV_PATH:
    raise RuntimeError('No "RASPI_PROV" environment variable detected.')

def update_wifi(ssid, passwd):
    with open(f'{RASPI_PROV_PATH}/wpa_suppplicant.template') as i, \
         open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as o:
             template = i.readlines()
             template[-3] = template[-3].replace('SSID', ssid)
             template[-4] = template[-4].replace('PASSWORD', passwd)
             o.writelines(template)

def get_current_wifi():
    with open('/etc/wpa_supplicant/wpa_supplicant.conf') as f:
         conf = f.readlines()
         ssid = re.search('"(.+)"\\n', confo[-3]).group(1)
         passwd = re.search('"(.+)"\\n', conf[-2]).group(1)
    return ssid, passwd

def get_current_ip(interface='wlan0'):
    ip = subprocess.check_output(['/sbin/ifconfig', f'{interface}', '|',
        'grep', '"inet"', '|',
        'cut', '-d:', '-f2', '|',
        'awk', '"{print $2}"'])
    if re.match('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', ip):
        return ip
    else:
        raise ValueError(f'No valid ip address assigned to interface: {interface}.')

def switch_AP_mode(active=True):
    if active:
        result = subprocess.check_output(['cp', f'{RASPI_PROV_PATH}/dhcpcd.conf.enable', '/etc/dhcpcd.conf'])
        result = subprocess.check_output(['/bin/systemctl', 'enable', 'hostapd'])
        result = subprocess.check_output(['/bin/systemctl', 'start', 'hostapd'])
        subprocess.check_output(['reboot'])
    else:
        result = subprocess.check_output(['cp', f'{RASPI_PROV_PATH}/dhcpcd.conf.disable', '/etc/dhcpcd.conf'])
        result = subprocess.check_output(['/bin/systemctl', 'stop', 'hostapd'])
        result = subprocess.check_output(['/bin/systemctl', 'disable', 'hostapd'])
        subprocess.check_output(['reboot'])
