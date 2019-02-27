#Externals
import time
import numpy as np
from PIL import ImageGrab #HACK: Negative coordinates are ignored by ImageGrab, (monitors left/up of primary)
import cv2
import pyautogui as pag

#Locals #TODO: figure the term for files written by me, in this place, vs files/modules? pulled in by npm magic
from Structs import *
import Win32Hooks as Hooks

global_game_coords = [0, 0, 0, 0]

def Init():
    print("Init")
    print("Getting Screen Bounds")
    GetBounds()

def GetBounds():
    global global_game_coords #huh
    Hooks.GetWindowRects();
    global_game_coords = Hooks.WindowRects[0];
    print("Screen Pos = left:{}, top:{}, right:{}, bot{}".format(global_game_coords[0], global_game_coords[1], global_game_coords[2], global_game_coords[3]))

#Move the mouse, check the pixel, click the button
def Logic(MousePos):
    windowpos = Hooks.GetWinPos(global_game_coords, MousePos)
    #print("X:{} Y:{}".format(windowpos[0], windowpos[1]))

    screen = np.array(ImageGrab.grab(bbox=global_game_coords))
    midpoint = Point(200,200)
    mid = Hooks.GetScreenPos(global_game_coords, midpoint)
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
        ap = Hooks.GetScreenPos(play_all_button)
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
            ap = Hooks.GetScreenPos(global_game_coords, card)

            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            ap = Hooks.GetScreenPos(global_game_coords, card_activate_button)
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
        ap = Hooks.GetScreenPos(global_game_coords, card)
        #pag.moveTo(ap[0], ap[1]) #white is a color where r> 100 and g > 100

        if (b == 255 and g < 200 and r < 200):
            card = Point(card_upgrade_line.x + counter + cardwidth / 5, card_upgrade_line.y)
            ap = Hooks.GetScreenPos(global_game_coords, card)

            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            ap = Hooks.GetScreenPos(global_game_coords, card_activate_button)
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
            ap = Hooks.GetScreenPos(global_game_coords, card)

            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)
            pag.click(ap[0], ap[1]) #white is a color where r> 100 and g > 100
            time.sleep(.1)

            ap = Hooks.GetScreenPos(global_game_coords, card_activate_button)
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
        ap = Hooks.GetScreenPos(end_turn_button)
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
        if (mouse_pos.x < global_game_coords[0] or mouse_pos.y < global_game_coords[1] or mouse_pos.x >= global_game_coords[2] or mouse_pos.y >= global_game_coords[3]):
            print("program paused")
            while True:
                if (mouse_pos.x > global_game_coords[0] and mouse_pos.y > global_game_coords[1] and mouse_pos.x < global_game_coords[2] and mouse_pos.y < global_game_coords[3]):
                    break
                mouse_pos = pag.position()
                time.sleep(1)
            print("program resumed")

        Logic(mouse_pos)
        time.sleep(20/100)#20 / 1000)

    return

Init()
MainLoop()
