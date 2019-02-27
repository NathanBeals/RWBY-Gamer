import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui as pag
import time
from win32 import win32gui

#HACK: only works on primary monitor, negative coords are ignored by screen grab

import win32gui

from ImportTest import Shark

game_coords = [0, 0, 0, 0]

def winEnumHandler( hwnd, ctx ):
    global game_coords;
    if win32gui.IsWindowVisible( hwnd ):
        #print(hex(hwnd), win32gui.GetWindowText( hwnd ))
        if (win32gui.GetWindowText(hwnd) == "RWBY Deckbuilding Game"):
            print(hex(hwnd), win32gui.GetWindowText( hwnd ))
            rect = win32gui.GetWindowRect(hwnd);
            game_coords[0] = rect[0]
            game_coords[1] = rect[1]
            game_coords[2] = rect[2]
            game_coords[3] = rect[3]

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def GetScreenPos(WindowPos): #TODO: better name
    global game_coords
    adjPos = [WindowPos.x + game_coords[0], WindowPos.y + game_coords[1]]
    return adjPos;

def GetWinPos(ScreenPos): #TODO: better name
    global game_coords
    adjPos = [ScreenPos.x - game_coords[0], ScreenPos.y - game_coords[1]]
    return adjPos;

def Init():
    print("Init")
    mylocalvar = Shark();
    mylocalvar.activate();
    print("Getting Screen Bounds")

    win32gui.EnumWindows( winEnumHandler, None );

    print("Screen Pos = left:{}, top:{}, right:{}, bot{}".format(game_coords[0], game_coords[1], game_coords[2], game_coords[3]))

#Move the mouse, check the pixel, click the button
def Logic(MousePos):
    windowpos = GetWinPos(MousePos)
    #print("X:{} Y:{}".format(windowpos[0], windowpos[1]))

    screen = np.array(ImageGrab.grab(bbox=game_coords))
    midpoint = Point(200,200)
    mid = GetScreenPos(midpoint)
    cardwidth = 150
    play_all_button = Point(330, 715)
    end_turn_button = Point(1478, 570)
    card_activate_button = Point(1160, 265)
    card_buy_line = Point(270, 280)
    card_buy_length = 1230 - 270;

    card_hand_effect_line = Point(520, 700);
    card_hand_effect_line_length = 1020 - 520;

    card_upgrade_line = Point(320, 522);
    card_upgrade_line_length = 1080 - 522;

    #Click play all button
    pixel = screen[play_all_button.y, play_all_button.x]
    #print("R:{}, G:{}, B{}\n".format(pixel[0], pixel[1], pixel[2]));

    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    if (r > 15 and r < 30 and g > 65 and g < 90 and b > 100 and b < 140):
        ap = GetScreenPos(play_all_button)
        pag.click(ap[0], ap[1])
        pag.moveTo(mid[0], mid[1])
        time.sleep(1)
        print("Play All Button Clicked")
        return



    #TODO: break into method calls (one for the line one for the klicking of effect cards)
    #Handle cards looking for effects and play them (pick a card from hand to respond)
    counter = 0
    while (counter < card_hand_effect_line_length):
        pixel = screen[card_hand_effect_line.y, card_hand_effect_line.x + counter]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        if ((b == 255 and g < 200 and r < 200) or (b==255 and g==255 and r==0) or (b > 60 and b < 100 and g > 180 and g < 220 and r < 220 and r > 180)):
            card = Point(card_hand_effect_line.x + counter + cardwidth / 5, card_hand_effect_line.y)
            ap = GetScreenPos(card)

            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            ap = GetScreenPos(card_activate_button)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            pag.moveTo(mid[0], mid[1])
            time.sleep(.1)

            print("Played Card")
            return
        counter += 1





    #look for upgradable cards and upgrade them
    counter = 0
    while (counter < card_upgrade_line_length):
        pixel = screen[card_upgrade_line.y, card_upgrade_line.x + counter]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        card = Point(card_upgrade_line.x + counter, card_upgrade_line.y)
        ap = GetScreenPos(card)
        #pag.moveTo(ap[0], ap[1]) #white is a color where r> 100 and g > 100

        if (b == 255 and g < 200 and r < 200):
            card = Point(card_upgrade_line.x + counter + cardwidth / 5, card_upgrade_line.y)
            ap = GetScreenPos(card)

            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            ap = GetScreenPos(card_activate_button)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            pag.moveTo(mid[0], mid[1])
            time.sleep(.1)

            print("Upgraded Card")
            return
        counter += 1





    #Look for buyable cards and buy them
    counter = 0
    while (counter < card_buy_length):
        pixel = screen[card_buy_line.y, card_buy_line.x + counter]

        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        if ((r > 250 and g > 250 and b > 90 and b < 110) or (r < 150 and g>230 and b>230) or (b==255 and r > 150 and r < 250 and g < 100)):
            card = Point(card_buy_line.x + counter + cardwidth / 5, card_buy_line.y)
            ap = GetScreenPos(card)

            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            ap = GetScreenPos(card_activate_button)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            pag.moveTo(mid[0], mid[1])
            time.sleep(.1)

            print("Bought Card")
            return
        counter += 1

    #return #early return



    #click end turn button
    pixel = screen[end_turn_button.y, end_turn_button.x]
    print("R:{}, G:{}, B{}\n".format(pixel[0], pixel[1], pixel[2]));

    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    if (r > 0 and r < 50 and g > 50 and g < 100 and b > 80 and b < 140):
        ap = GetScreenPos(end_turn_button)
        pag.moveTo(ap[0], ap[1])
        pag.mouseDown()
        time.sleep(1)
        pag.mouseUp()
        pag.moveTo(mid[0], mid[1])
        time.sleep(1)
        print("End Turn Button Pressed")
        return

    return

def MainLoop():
    print("MainLoop")
    while True:
        mouse_pos = pag.position()

        #only run the application while the mouse is in the window area
        if (mouse_pos.x < game_coords[0] or mouse_pos.y < game_coords[1] or mouse_pos.x >= game_coords[2] or mouse_pos.y >= game_coords[3]):
            print("program paused")
            while True:
                if (mouse_pos.x > game_coords[0] and mouse_pos.y > game_coords[1] and mouse_pos.x < game_coords[2] and mouse_pos.y < game_coords[3]):
                    break
                mouse_pos = pag.position()
                time.sleep(1)
            print("program resumed")

        Logic(mouse_pos)
        time.sleep(20/100)#20 / 1000)

    return

Init()
MainLoop()
