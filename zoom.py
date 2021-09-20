import time
import subprocess 
import webbrowser

def Openzoom():
    subprocess.Popen(r"C:\Program Files (x86)\Zoom\bin\Zoom.exe") # path might be different for different users
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
