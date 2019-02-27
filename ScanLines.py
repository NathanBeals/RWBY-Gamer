#Hack: wait why did I split it into 4 variables? I was using Points
#TODO: point should really contain valid or not
import numpy as np
from Structs import *

class HScanLine: #TODO: I might be able to make this a any line a to b pretty easitly
    def __init__(self, origin, end):
        self.ox = origin.x
        self.oy = origin.y
        self.ex = end.x
        self.ey = end.y

    #TODO: update list to take an array of color ranges
    def ScanLine(self, screen, highColor, lowColor, increment):
        if (increment < 1): return Point(-1,-1) #infinite loop escape

        counter = 0;
        while (self.ox + counter * increment <= self.ex):
            pixel = screen[self.oy, self.ox + counter] #screen is y,x
            pixelColor = RGB(pixel[0], pixel[1], pixel[2])

            #return the Point if it's in the proper color range
            #print("pixel {}{} , color {} {} {}", self.ox + counter, self.oy, pixelColor.r, pixelColor.g, pixelColor.b)
            if (pixelColor.IsInRange(highColor, lowColor)):
                print("Color Match")
                print("{}{}", self.ox, self.oy)
                return Point(self.ox + counter, self.oy);
            counter += 1

        return Point(-1, -1) #did not find result

    #Hack: not a great solution, need a way to indicate failure, I suppose I could handle it the windows way but, consider
    def IsValidResult(self, position):
        return False if (position == Point(-1, -1)) else True;
