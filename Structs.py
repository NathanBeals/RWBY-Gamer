#class name is bad almost immediately, I want ScanLine to be in here
#but i also want scanline to have a method called... scanline? WalkLineForCondition (colors)
#TODO: add method to Scanline that walks the line looking for a color and returns a point where the condition is true or the endpoint

class Shark:
    def activate(self):
        print("Active")

class Point: #consider isinstance self.__class__
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not __eq__(self, other)

class RGB:
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    def IsInRange(self, LowRGB, HighRGB):
        if (self.r > HighRGB.r or self.r < LowRGB.r): return False
        if (self.g > HighRGB.g or self.g < LowRGB.g): return False
        if (self.b > HighRGB.b or self.b < LowRGB.b): return False
        return True
