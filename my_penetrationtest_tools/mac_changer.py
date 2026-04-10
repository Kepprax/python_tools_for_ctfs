import optparse
import subprocess
import re


parse_object = optparse.OptionParser(usage="python %prog -i <interface> -m <new_mac_address>")

def get_user_input():
    parse_object=optparse.OptionParser()
    parse_object.add_option("-i","--interface",dest="interface")
    parse_object.add_option("-m","--mac",dest="mac_address")

    return parse_object.parse_args()

#user_interface=user_inputs.interface
#user_mac_address=user_inputs.mac_address

def change_mac_addres(user_interface,user_mac_address):
    subprocess.call(["ifconfig",user_interface,"down"])
    subprocess.call(["ifconfig",user_interface,"hw","ether",user_mac_address])
    subprocess.call(["ifconfig",user_interface,"up"])

    #Buraya kadar başarılı ama burdan sonra mac adresi değiştiği için dhcp protokü çalışmıyor yeni mac adresine
    #ıp atmıyor bu yüzden aşağıdaki kodlara ihtiyacımız var

    result = subprocess.call(["dhclient", user_interface])
    if result != 0:
        print("[-] dhclient başarısız oldu. Yetki eksikliği olabilir ya da interface ismi yanlış.")
    else:
        print("[+] IP adresi başarıyla alındı.")

    #subprocess.call(["dhclient", user_interface])  # Bu satırı ekledim ama hata aldım

def control_new_mac_address(interface):
    ifconfig=subprocess.check_output(["ifconfig",interface]).decode('utf-8')
    new_mac=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig)

    if new_mac:
        return new_mac.group(0)
    else :
        return None

print("mac chanager started")

(user_input,arguments)=get_user_input()
change_mac_addres(user_input.interface,user_input.mac_address)
finalized_mac=control_new_mac_address(user_input.interface)

if finalized_mac==user_input.mac_address:
    print("mac has changed succsefully ")
else :
    print("Error!")




