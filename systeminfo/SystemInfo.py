import sys
import os
import psutil
import platform
import GPUtil
from datetime import datetime

#for cmd based info
import subprocess

#for ip
import socket

import urllib
from urllib.request import Request, urlopen


def adjust_size(size):
    factor = 1024
    for i in ["B", "KB", "MB", "GB", "TB"]:
        if size > factor:
            size = size / factor
        else:
            return f"{size:.3f}{i}"

class os_info():
    def os_name():
        return platform.system()

    def os_release():
        return platform.release()
        #run on a Windows 10 Computer it returns 10

    def os_version():
        uname = platform.uname()
        return uname.version
        #run on a Window 10 Computer it returns the exact Version for example 10.0.22621

class device_info():
    def device_name():
        return platform.node()

    def machine():
        return platform.machine()

    def platform():
        return platform.platform()

    #only for windows
    def hwid():
        return str(subprocess.check_output("wmic csproduct get uuid"), "utf-8").split("\n")[1].strip()

    def model():
        return str(subprocess.check_output("wmic computersystem get model"), "utf-8").split("\n")[1].strip()

    def computer_manufacturer():
        return str(subprocess.check_output("wmic computersystem get manufacturer"), "utf-8").split("\n")[1].strip()

    def systemtype():
        return str(subprocess.check_output("wmic computersystem get systemtype"), "utf-8").split("\n")[1].strip()

class cpu_info():
    def processor_name():
        return platform.processor()

    def cpu_number():
        return os.cpu_count()

    def cpu_number_pysical():
        return psutil.cpu_count(logical=False)

    def cpu_number_logical():
        return psutil.cpu_count(logical=True)

    def cpu_max_frequency():
        return psutil.cpu_freq().max

    def cpu_current_frequency():
        return psutil.cpu_freq().current

    def cpu_usage():
        return psutil.cpu_percent()

    def cpu_usage_core():
        cores = {}
        for i, perc in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cores[i] = perc
        return cores

class gpu_info():
    def get_gpus():
        return GPUtil.getGPUs()

    def gpu_info_id(gpu):
        return gpu.id

    def gpu_info_name(gpu):
        return gpu.name

    def gpu_info_load(gpu):
        return gpu.load*100

    def gpu_info_memory_free(gpu):
        return gpu.memoryFree

    def gpu_info_memory_used(gpu):
        return gpu.memoryUsed

    def gpu_info_memory_total(gpu):
        return gpu.memoryTotal

    def gpu_info_temperature(gpu):
        return gpu.temperature

    def gpu_info():
        gpus = gpu_info.get_gpus()
        gpu_dict = {}
        for gpu in gpus:
            gpu_dict[gpu_info.gpu_info_name(gpu)] = str(gpu_info.gpu_info_id(gpu))

        return gpu_dict

class ram_info():
    def get_ram():
        return psutil.virtual_memory()

    def ram_total():
        virtual_mem = psutil.virtual_memory()
        return adjust_size(virtual_mem.total)

    def ram_available():
        virtual_mem = psutil.virtual_memory()
        return adjust_size(virtual_mem.available)

    def ram_used():
        virtual_mem = psutil.virtual_memory()
        return adjust_size(virtual_mem.used)

    def ram_used_percentage():
        virtual_mem = psutil.virtual_memory()
        return virtual_mem.percent

class swap_info():
    def get_swap():
        return psutil.swap_memory()

    def swap_total():
        swap = psutil.swap_memory()
        return adjust_size(swap.total)

    def swap_free():
        swap = psutil.swap_memory()
        return adjust_size(swap.free)

    def swap_used():
        swap = psutil.swap_memory()
        return adjust_size(swap.used)

    def swap_used_percentage():
        swap = psutil.swap_memory()
        return swap.percent

class system():
    def process_id():
        return os.getpid()

    def os_getenv(key):
        return os.getenv(key)

    def os_environ_get(key):
        return os.environ.get(key)

    def boot_time():
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        return f"{bt.day}.{bt.month}.{bt.year} {bt.hour}:{bt.minute}:{bt.second}"

    def username():
        return system.os_environ_get("USERNAME")

    def systeminfos():
        infos = str(subprocess.check_output("systeminfo"), "utf-8").replace("\r", "").replace(" ", "#").split("\n")
        systeminfos = {}
        for i in range(0, len(infos) - 1):
            temp = infos[i]
            t = temp.split(":")
            if (len(t) >= 2):
                temp = str(t[1][::-1].rstrip("#"))[::-1]
                systeminfos[t[0].replace("#", " ")] = temp.replace("#", " ")
        return systeminfos

    def systeminfo():
        return str(subprocess.check_output("systeminfo"), "utf-8")

class disk_info():
    def get_disk():
        return psutil.disk_partitions()

    def disk_info_name(p):
        return p.device

    def disk_info_moutpoint(p):
        return p.mountpoint

    def disk_file_system_type(p):
        return p.fstype

    def partition_total_size(p):
        try:
            partition_usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            return
        return adjust_size(partition_usage.total)

    def partition_used(p):
        try:
            partition_usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            return
        return adjust_size(partition_usage.used)

    def partition_free(p):
        try:
            partition_usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            return
        return adjust_size(partition_usage.free)

    def partition_percentage(p):
        try:
            partition_usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            return
        return partition_usage.percent

    def all_disk_read_since_boot():
        disk_io = psutil.disk_io_counters()
        return adjust_size(disk_io.read_bytes)

    def all_disk_write_since_boot():
        disk_io = psutil.disk_io_counters()
        return adjust_size(disk_io.write_bytes)

class network_info():
    def get_network():
        return psutil.net_if_addrs()

    def get_adress(address):
        return address.address

    def received_since_boot():
        net_io = psutil.net_io_counters()
        return adjust_size(net_io.bytes_recv)

    def send_since_boot():
        net_io = psutil.net_io_counters()
        return adjust_size(net_io.bytes_sent)

    def get_network_information():
        network_name = []
        network_address = {}
        network_netmask = {}
        network_family = {}
        network_broadcast_ip = {}
        network_mac_address = {}
        network_broadcast_mac = {}

        if_addrs = network_info.get_network()

        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                network_name.append(interface_name)
                #print(f"Interface: {interface_name}")
                network_family[interface_name] = str(address.family)
                if str(address.family) == 'AddressFamily.AF_INET':
                    network_address[interface_name] = str(address.address)
                    network_netmask[interface_name]  = str(address.netmask)
                    network_broadcast_ip[interface_name] = str(address.broadcast)
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    network_mac_address[interface_name] = str(address.address)
                    network_netmask[interface_name] = str(address.netmask)
                    network_broadcast_mac[interface_name] = str(address.broadcast)
        return network_name, network_address, network_netmask, network_family, network_broadcast_ip, network_mac_address, network_broadcast_mac

    def internet_connection():
        if "The wireless local area network interface is powered down and doesn't support the requested operation." in str(subprocess.getoutput('cmd /c "netsh wlan show networks"')):
            return False
        else:
            return True

    def public_ip():
        try:
            return urlopen(Request("https://api.ipify.org/")).read().decode().strip()
        except urllib.error.URLError:
            return False

    def ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("google.com", 80))
            return s.getsockname()[0]
        except socket.gaierror:
            return False

class windows():
    def APPDATA():
        return system.os_getenv("APPDATA")

    def LOCAL_APPDATA():
        return system.os_getenv("LOCALAPPDATA")

def network():
    print("-" * 40, "Network Information", "-" * 40)
    if_addrs = network_info.get_network()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"Interface: {interface_name}")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")

def info():
    print("-"*45, "Start", "-"*45)
    print("-"*40, "Sys Info", "-"*40)
    print(f"Node Name: {device_info.device_name()}")
    print(f"OS: {os_info.os_name()}")
    print(f"Release: {os_info.os_release()}")
    print(f"Version: {os_info.os_version()}")
    print(f"Machine: {device_info.machine()}")
    print(f"Processor: {cpu_info.processor_name()}")

    print("-"*40, "Boot Time", "-"*40)
    print(f"Boot Time:{system.boot_time()}")

    print("-"*40, "CPU Info", "-"*40)
    print("Actual Cores:", cpu_info.cpu_number_pysical())
    print("Logical Cores:", cpu_info.cpu_number_logical())
    print(f"Max Frequency: {cpu_info.cpu_max_frequency()}Mhz")
    print(f"Current Frequency: {cpu_info.cpu_current_frequency()}Mhz")
    print(f"CPU Usage: {cpu_info.cpu_usage()}%")
    cores = cpu_info.cpu_usage_core()
    for i in range(0, len(cores)):
        print(f"Core {i + 1}: {cores[i]}%")

    print("-"*40, "RAM Info", "-"*40)
    print(f"Total: {ram_info.ram_total()}")
    print(f"Available: {ram_info.ram_available()}")
    print(f"Used: {ram_info.ram_used()}")
    print(f"Percentage: {ram_info.ram_used_percentage()}%")

    print("-"*40, "SWAP", "-"*40)
    print(f"Total: {swap_info.swap_total()}")
    print(f"Free: {swap_info.swap_free()}")
    print(f"Used: {swap_info.swap_used()}")
    print(f"Percentage: {swap_info.swap_used_percentage()}%")

    print("-"*40, "Disk Information", "-"*40)
    partitions = disk_info.get_disk()
    for p in partitions:
        print(f"Device: {disk_info.disk_info_name(p)}")
        print(f"\tMountpoint: {disk_info.disk_info_moutpoint(p)}")
        print(f"\tFile system type: {disk_info.disk_file_system_type(p)}")

        print(f"  Total Size: {disk_info.partition_total_size(p)}")
        print(f"  Used: {disk_info.partition_used(p)}")
        print(f"  Free: {disk_info.partition_free(p)}")
        print(f"  Percentage: {disk_info.partition_percentage(p)}%")

    print(f"Read since boot: {disk_info.all_disk_read_since_boot()}")
    print(f"Written since boot: {disk_info.all_disk_write_since_boot()}")

    print("-"*40, "GPU Details", "-"*40)
    gpus = gpu_info.get_gpus()
    for gpu in gpus:
        print(f"ID: {gpu_info.gpu_info_id(gpu)}, Name: {gpu_info.gpu_info_name(gpu)}")
        print(f"\tLoad: {gpu_info.gpu_info_id(gpu)}%")
        print(f"\tFree Mem: {gpu_info.gpu_info_memory_free(gpu)}MB")
        print(f"\tUsed Mem: {gpu_info.gpu_info_memory_used(gpu)}MB")
        print(f"\tTotal Mem: {gpu_info.gpu_info_memory_total(gpu)}MB")
        print(f"\tTemperature: {gpu_info.gpu_info_temperature(gpu)} °C")

    print("-" * 40, "Network Information", "-" * 40)
    network_name, network_address, network_netmask, network_family, network_broadcast_ip, network_mac_address, network_broadcast_mac = network_info.get_network_information()

    for i in range(0, len(network_name)):
        network_name_not_list = network_name[i]
        print(f"Interface: {network_name[i]}")
        if str(network_family[network_name_not_list]) == 'AddressFamily.AF_INET' or str(network_family[network_name_not_list]) == 'AddressFamily.AF_INET6' or str(network_family[network_name_not_list]) == 'AddressFamily.AF_INET4':
            print(f"  IP Address: {network_address[network_name_not_list]}")
            print(f"  Netmask: {network_netmask[network_name_not_list]}")
            print(f"  Broadcast IP: {network_broadcast_ip[network_name_not_list]}")

        elif str(network_family[network_name_not_list]) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {network_mac_address[network_name_not_list]}")
                print(f"  Netmask: {network_netmask[network_name_not_list]}")
                print(f"  Broadcast MAC: {network_broadcast_mac[network_name_not_list]}")

    print(f"Total Bytes Sent: {network_info.send_since_boot()}")
    print(f"Total Bytes Received: {network_info.received_since_boot()}")

    print("-" * 40, "Computer", "-" * 40)
    if(os_info.os_name() == "Windows"):
        print(f"PC Hardware ID (hwid): {device_info.hwid()}")
        print(f"PC Model: {device_info.model()}")
        print(f"PC manufacturer: {device_info.computer_manufacturer()}")
        print(f"PC Systemtype: {device_info.systemtype()}")

    print("-" * 40, "INTERNET CONNECTION", "-" * 40)
    print(f"Internet connection? {network_info.internet_connection()}")
    INTERNET_CONNECTION = network_info.internet_connection()
    if (INTERNET_CONNECTION):
        print(f"PUBLIC IP: {network_info.public_ip()}")
        print(f"IP: {network_info.ip()}")


    print("-" * 40, "SYSTEM INFO", "-" * 40)
    print(system.systeminfo())

    network()


if __name__ == '__main__':
    info()