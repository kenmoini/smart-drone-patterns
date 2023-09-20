import wifi
import os
#import time

# scan for available WiFi networks
wirelessInterface = os.environ.get("WIRELESS_IFACE", "wbr0")
wifi_scanner = wifi.Cell.all(wirelessInterface)

wirelessAccessPoint = os.environ.get("WIRELESS_AP", "TELLO-9AFD00")
available_networks = [cell.ssid for cell in wifi_scanner]

# print available networks
print(f"Available Networks: {available_networks}")

# connect to a WiFi network
#network_ssid = input("Enter network SSID: ")
#network_pass = input("Enter network password: ")



#for cell in wifi_scanner:
#    if cell.ssid == network_ssid:
#        scheme = wifi.Scheme.for_cell(wirelessInterface, cell.ssid, cell, network_pass)
#        scheme.save()
#        scheme.activate()
#        print(f"Connected to network: {network_ssid}")
#        break
#else:
#	print(f"Unable to find network: {network_ssid}")