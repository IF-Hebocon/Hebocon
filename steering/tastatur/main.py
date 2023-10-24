from serial import Serial
from pynput.keyboard import Listener, Key
from time import sleep

siri = Serial(port='COM4', baudrate=9600, timeout=.1)

keys = { 'w': 1,
         'a': 2, 
         's': 3, 
         'd': 4 }

key_pressed = None

def on_press(key):
        if key is Key.esc:
            siri.close()
            exit()
        if hasattr(key, 'char'):
            if key.char in keys.keys() and key_pressed == None:
                key_pressed = key.char
                siri.write(bytes(str(keys[key.char]), 'utf-8'))

def on_release(key):
        if hasattr(key, 'char'):
            if key.char in keys.keys() and key.char == key_pressed:
                siri.write(bytes(str(5), 'utf-8'))
                key_pressed = None

def main():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    print("Programm startet...")
    sleep(2)
    print("Programm gestartet! Drücke ESC zum beenden")
    main()
