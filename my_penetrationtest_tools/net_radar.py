import scapy.all as scapy
import optparse

#pathway
#1-arp request
#2-broadcast
#3-request

def get_user_input():
    parse_object=optparse.OptionParser()
    parse_object.add_option("-r","--range",dest="ip_address",help="enter your ip adress with last octet 0/24")
    (user_input,arguments)=parse_object.parse_args()
    if not user_input.ip_address:
        print("Enter IP adress ")
    return user_input

def scan_network(ip):
    arp_request_packet=scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP()) // to control arp funciton
    broadcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether()) // to control broadcast, same exactly arp function
    combined_packet=broadcast_packet/arp_request_packet
    #it's scapy's funcitons using "/" we can combine two packet
    (answered_list,unanswered_list)=scapy.srp(combined_packet,timeout=1)
    answered_list.summary()
    # if we want only important information thanks to scapy we don't need regex

user_ip_address=get_user_input()
scan_network(user_ip_address.ip_address)

