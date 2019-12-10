import win32gui
import re

# handle = win32gui.FindWindow("Mabinogi", None) 
# print(handle)

winList = []
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        clsname = win32gui.GetClassName(hwnd)
        if (clsname == 'Mabinogi'):
            title = win32gui.GetWindowText(hwnd)
            winList.append(title)

win32gui.EnumWindows(get_all_hwnd, 0)
# print(winList)

checkList = []
for i in range(0, 11):
    checkList.append(False)

for row in winList:
    channel = re.findall('\[CHANNEL[0-9]{1,2}\]', row)[0]
    id = re.findall('[0-9]{1,2}', channel)[0]
    id = int(id)
    if (id >= 0 and id <= 11):
        checkList[id - 1] = True
    
print(checkList)
