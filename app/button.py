from cmu_graphics import *
import math

class Button:
    def __init__(self, name, left, top, width, height, shape='rect'):
        self.name = name 
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.bottom = self.top + self.height
        self.right = self.left + self.width
        self.color = 'white'
        self.shape = shape

    def mouseOver(self, x, y):
        if self.shape == 'rect':
            if self.left <= x <= self.right and self.top <= y <= self.bottom:
                return True
        elif self.shape == 'oval':
            # from https://www.geeksforgeeks.org/check-if-a-point-is-inside-outside-or-on-the-ellipse/
            # (x-h)^2/a^2 + (y-k)^2/b^2 <= 1
            a = self.width / 2
            b = self.height / 2
            h = self.left + a
            k = self.top + b

            return (x-h)**2/a**2 + (y - k)**2/b**2 <= 1
        return False
    
    def draw(self):
        if self.shape == 'rect':
            drawRect(self.left, self.top, self.width, self.height, 
                fill = self.color, border = 'black', borderWidth = 2)
        elif self.shape == 'oval':
            drawOval(self.left + self.width /2, self.top + self.height/2,
                     self.width, self.height, fill = self.color, border = 'black', borderWidth = 2)

        drawLabel(self.name.capitalize(), self.left + self.width/2, 
            self.top + self.height/2, size = 20)
     