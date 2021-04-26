import time
import subprocess 
import webbrowser
import keyboard

def Openzoom():
    subprocess.Popen(r"C:\Users\vijay\AppData\Roaming\Zoom\bin\Zoom.exe")
    time.sleep(5)

def Openmeeting(meeting_url):
    webbrowser.open_new_tab(meeting_url)
    time.sleep(1)

def Closemeeting():
    try:
        subprocess.call(["taskkill","/F","/IM","Zoom.exe"])
        time.sleep(2)

    finally:
        pass
