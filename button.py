from cmu_graphics import *
import time
from datetime import datetime, timedelta
import math
        
class TimerLabel:
    def __init__(self, text, left, top):
        self.text = text
        self.left = left
        self.top = top
        self.time = time.time()

    def start(self):
        self.time = time.time()

    def elapsed(self):
        return timedelta(seconds=int(time.time() - self.time))

    def draw(self):
        # https://www.geeksforgeeks.org/python-datetime-timedelta-function/
        # https://www.geeksforgeeks.org/format-a-number-width-in-python/
        e = self.elapsed()
        text = f'{self.text}: {e.seconds//60:02d}:{e.seconds%60:02d}'
        drawLabel(text, self.left, self.top)

class LabelButton:
    def __init__(self, text, l, t, color, border, borderWidth=2, opacity=70, size=60):
        self.text = text
        self.l = l
        self.t = t
        self.color = color
        self.border = border
        self.borderWidth = borderWidth
        self.opacity = opacity
        self.isSelected = False
        self.size = size

    def mouseOver(self, x, y):
        if self.l-60 <= x <= self.l + 60 and self.t -40 <= y <= self.t + 40:
            self.isSelected = True
        else:
            self.isSelected = False
        return self.isSelected

    def draw(self):
        text = self.text
        opacity = self.opacity
        left = self.l
        if self.isSelected:
            text = f"[{self.text}]"
            opacity = 100
            left -= 1

        drawLabel(text, left, self.t, font='cinzel',
                  size=self.size, fill=self.color, border=self.border, borderWidth=self.borderWidth,
                  opacity=opacity)

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
     