from serial import Serial
from pynput.keyboard import Listener, Key
from time import sleep

siri = Serial(port='COM4', baudrate=9600, timeout=.1)

keys = { 'w': 1, 
         'a': 2, 
         's': 3, 
         'd': 4 }

def on_press(key):
        if key is Key.esc:
            siri.close()
            exit()
        if hasattr(key, 'char'):
            if key.char in keys.keys():
                siri.write(bytes(str(keys[key.char]), 'utf-8'))

def main():
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    print("Programm startet...")
    sleep(2)
    print("Programm gestartet! Drücke ESC zum beenden")
    main()