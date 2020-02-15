import psutil
import re
import win32gui
import win32process

winList = []
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        clsname = win32gui.GetClassName(hwnd)
        if (clsname == 'Mabinogi'):
            title = win32gui.GetWindowText(hwnd)

            tid, pid = win32process.GetWindowThreadProcessId(hwnd)
            p = psutil.Process(pid)
            c = p.connections()
            connectInfo = 'No Connect'
            if (len(c) > 0 and not re.findall("Nosound", title)):
                connectInfo = str(c[0].raddr)
                winList.append(pid)
                print("hwnd:%d, Title:%s, pid:%d, conn:%s"%(hwnd, title, pid, connectInfo))

win32gui.EnumWindows(get_all_hwnd, 0)
# print(winList)

# def findProcessIdByName(processName):
#     '''
#     Get a list of all the PIDs of a all the running process whose name contains
#     the given string processName
#     '''
 
#     listOfProcessObjects = []
 
#     #Iterate over the all the running process
#     for proc in psutil.process_iter():
#        try:
#            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
#            # Check if process name contains the given name string.
#            if processName.lower() in pinfo['name'].lower():
#                listOfProcessObjects.append(pinfo)
#        except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
#            pass
 
#     return listOfProcessObjects

# listOfProcessIds = findProcessIdByName('Client.exe')

for pid in winList:
    p = psutil.Process(pid)
    p.cpu_affinity([0,1,2,3,4,5,6,7])
