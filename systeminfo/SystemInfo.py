import sys
import os
import psutil
import platform
import GPUtil
from datetime import datetime


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
        uname = platform.uname()
        return uname.node

    def machine():
        uname = platform.uname()
        return uname.machine

class cpu_info():
    def processor_info():
        uname = platform.uname()
        return uname.processor

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

    def boot_time():
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        return f"{bt.day}.{bt.month}.{bt.year} {bt.hour}:{bt.minute}:{bt.second}"

class disk_info():
    def get_disk():
        return psutil.disk_partitions()

    def disk_info_name(p):
        return p.device

    def disk_info_moutpoint(p):
        return p.mountpoint

    def disk_file_system_type(p):
        p.fstype

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
        network_family =  {}
        network_broadcast_ip = {}
        network_mac_address = {}
        network_broadcast_mac = {}

        if_addrs = psutil.net_if_addrs()

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
