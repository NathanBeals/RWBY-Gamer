#TODO: I'd still rather remove the global variable and just have GetWindowRects return the list of window rects but I'm uncertain
# of how to syntax my way into passing an new empty array to the winEnumHanlder delegate.
from win32 import win32gui

global WindowRects

def winEnumHandler( hwnd, ctx):
    global WindowRects;
    if win32gui.IsWindowVisible( hwnd ):
        #print(hex(hwnd), win32gui.GetWindowText( hwnd ))
        if (win32gui.GetWindowText(hwnd) == "RWBY Deckbuilding Game"):
            print(hex(hwnd), win32gui.GetWindowText( hwnd ))
            rect = win32gui.GetWindowRect(hwnd);
            winRect = [0,0,0,0]
            winRect[0] = rect[0]
            winRect[1] = rect[1]
            winRect[2] = rect[2]
            winRect[3] = rect[3]
            WindowRects.append(winRect);

def GetWindowRects():
    global WindowRects;
    WindowRects = []
    win32gui.EnumWindows( winEnumHandler, None )

def GetScreenPos(WinRect, WinPos): #TODO: better name
    adjPos = [WinPos.x + WinRect[0], WinPos.y + WinRect[1]]
    return adjPos;

def GetWinPos(WinRect, ScreenPos): #TODO: better name
    adjPos = [ScreenPos.x - WinRect[0], ScreenPos.y - WinRect[1]]
    return adjPos;
