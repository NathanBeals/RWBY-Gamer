#TODO: make a start turn signal

#Externals
import time
import numpy as np
from PIL import ImageGrab #HACK: Negative coordinates are ignored by ImageGrab, (monitors left/up of primary)
import cv2
import pyautogui as pag

#Locals #TODO: figure the term for files written by me, in this place, vs files/modules? pulled in by npm magic
from Structs import *
import ScanLines as SL
import Win32Hooks as Hooks

global_game_coords = [0, 0, 0, 0] #TODO: multiple windows, remove global

def Init():
    print("Init")
    print("Getting Screen Bounds")
    GetBounds() #turns out I can just place this definition anywhere, neat

def GetBounds():
    global global_game_coords #huh
    Hooks.GetWindowRects();
    global_game_coords = Hooks.WindowRects[0];
    print("Screen Pos = left:{}, top:{}, right:{}, bot{}".format(global_game_coords[0], global_game_coords[1], global_game_coords[2], global_game_coords[3]))

#TODO: replace these "double clicks" with a call to double click, I bet there is an actuall delay I can add there

def ActivateCard(cardEdge, cardOffset, activateButton, restPosition):
    card = Point(cardEdge.x + cardOffset, cardEdge.y)
    ap = Hooks.GetScreenPos(global_game_coords, card)

    #click card (doubleclick doesn't register so delayed click, although thinking of it now)
    pag.click(ap.x, ap.y)
    time.sleep(.1)
    pag.click(ap.x, ap.y)
    time.sleep(.1)

    #click activate
    ap = Hooks.GetScreenPos(global_game_coords, activateButton)
    pag.click(ap.x, ap.y)
    time.sleep(.1)
    pag.click(ap.x, ap.y)
    time.sleep(.1)

    #rest
    pag.moveTo(restPosition.x, restPosition.y)
    time.sleep(.1)

    return

#Move the mouse, check the pixel, click the button
def Logic(MousePos): #HACK: passing mouse position is rather limiting, consider
    windowpos = Hooks.GetWinPos(global_game_coords, MousePos)
    #print("X:{} Y:{}".format(windowpos[0], windowpos[1]))

    #Variable Declarations? #HACK: move to seperate file
    screen = np.array(ImageGrab.grab(bbox=global_game_coords))
    rest = Hooks.GetScreenPos(global_game_coords, Point(100,150))
    play_all_button = Point(330, 715)
    end_turn_button = Point(1478, 570)
    card_activate_button = Point(1160, 265)

    #reset
    pag.moveTo(rest.x, rest.y)
    pag.click();

    #Click play all button
    play_all_scan = SL.HScanLine(Point(330, 715), Point(331, 715));
    resultP = play_all_scan.ScanLine(screen, RGB(15,65,100), RGB(30,90,140), 1);
    if (play_all_scan.IsValidResult(resultP)):
        ap = Hooks.GetScreenPos(global_game_coords, resultP)
        pag.click(ap.x, ap.y)
        pag.moveTo(rest.x, rest.y)
        time.sleep(2)
        print("Play All Button Clicked")
        return


    #Try to Buy the Boss
    #1389, 248 //check for color 40-70r, 0-20g, 90-120b
    #785,730 -> buy boss Button
    boss_scan = SL.HScanLine(Point(1390, 248), Point(1420, 248));
    resultP = boss_scan.ScanLine(screen, RGB(40,0,90), RGB(70,20,120), 1);
    if (boss_scan.IsValidResult(resultP)):
        #click boss
        ap = Hooks.GetScreenPos(global_game_coords, Point(1480, 375))
        pag.click(ap.x, ap.y)
        time.sleep(.1)
        #click buy boss
        ap = Hooks.GetScreenPos(global_game_coords, Point(785,730))
        pag.moveTo(ap.x, ap.y)
        pag.click(ap.x, ap.y)
        time.sleep(5)
        #wait for animation
        pag.moveTo(rest.x, rest.y)
        time.sleep(.1)
        print("Play All Button Clicked")
        return


    #Handle Card Effects (in hand)
    card_hand_effect_scan = SL.HScanLine(Point(520, 700), Point(1120, 700))
    #Blue
    resultP = card_hand_effect_scan.ScanLine(screen, RGB(200,200,255), RGB(240,255,255), 1)
    if (card_hand_effect_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Played Card")
        return
    #Blue also
    resultP = card_hand_effect_scan.ScanLine(screen, RGB(0,255,255), RGB(0,255,255), 1)
    if (card_hand_effect_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Played Card")
        return
    #Yellow?
    resultP = card_hand_effect_scan.ScanLine(screen, RGB(180,180,60), RGB(220,220,100), 1)
    if (card_hand_effect_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Played Card")
        return
    #Purple?
    resultP = card_hand_effect_scan.ScanLine(screen, RGB(200,20,240), RGB(255,60,255), 1)
    if (card_hand_effect_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Played Card")
        return
    #Orange
    resultP = card_hand_effect_scan.ScanLine(screen, RGB(210,70,70), RGB(255,100,100), 1)
    if (card_hand_effect_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Played Card")
        return


    #Look for upgradable cards and upgrade them
    play_area_scan = SL.HScanLine(Point(300, 620), Point(1080, 620))
    resultP = play_area_scan.ScanLine(screen, RGB(50,50,255), RGB(254,254,255), 1)
    if (play_area_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 30, card_activate_button, rest)
        print("Upgraded Card")
        return


    #Buy cards (and handle effects in the buy area)
    buy_area_scan = SL.HScanLine(Point(270, 460), Point(1250, 460)) #bottom of card
    resultP = buy_area_scan.ScanLine(screen, RGB(250,250,90), RGB(255,255,130), 1)
    if (buy_area_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Bought Card") # not accurate name but good for testing the line
        return

        #This one is causeing problems
        #it's a light blue that happens when a card is going to be placed on the top of deck after purchase
        #the issue is some cards can also be a very similar shade of this blue, neither is a super common thing (5ish cards are the color, 4 ish cards cause the color)
        #or maybe it's purple, wah
        #no wait I think this was coverting white gosh durnit
        #the buy area is complex
        #and now I made it purple
    resultP = buy_area_scan.ScanLine(screen, RGB(255,20,255), RGB(255,70,255), 1)
    if (buy_area_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Bought Card")
        return

    resultP = buy_area_scan.ScanLine(screen, RGB(150,100,255), RGB(250,255,255), 1)
    if (buy_area_scan.IsValidResult(resultP)):
        ActivateCard(resultP, 50, card_activate_button, rest)
        print("Bought Card")
        return


    #click end turn button (has to be held down on occasion)
    end_turn_scan = SL.HScanLine(Point(1478, 570), Point(1479, 570))
    resultP = end_turn_scan.ScanLine(screen, RGB(0,50,80), RGB(50,100,140), 1)
    if (end_turn_scan.IsValidResult(resultP)):
        ap = Hooks.GetScreenPos(global_game_coords, resultP)
        pag.moveTo(ap.x, ap.y)
        pag.mouseDown()
        time.sleep(.1)
        pag.mouseUp()
        pag.moveTo(rest.x, rest.y)
        time.sleep(.1)
        print("Played Card")
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
                time.sleep(.1)
            print("program resumed")

        Logic(mouse_pos)
        time.sleep(.5)#20 / 1000)

    return


#Excecution
Init()
MainLoop()
#End
