from systeminfo.SystemInfo import *

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
    print(f"Processor: {cpu_info.processor_info()}")

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

    network()


if __name__ == '__main__':
    info()