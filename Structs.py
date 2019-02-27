#class name is bad almost immediately, I want ScanLine to be in here
#but i also want scanline to have a method called... scanline? WalkLineForCondition (colors)
#TODO: add method to Scanline that walks the line looking for a color and returns a point where the condition is true or the endpoint


class Shark:
    def activate(self):
        print("Active")

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class ScanLine:
    def __init__(self, origin, end):
        self.ox = origin.x
        self.oy = origin.y
        self.ex = end.x
        self.ey = end.y
