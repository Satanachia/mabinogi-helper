import win32gui
import win32con

handle = win32gui.FindWindow("Mabinogi", None) 
print(handle)
win32gui.ShowWindow(handle, win32con.SW_SHOW)
