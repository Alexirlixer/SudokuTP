from cmu_graphics import *
import time
from datetime import datetime, timedelta
import math

class TimerLabel:
    def __init__(self, text, left, top,opacity=60, size=17):
        self.text = text
        self.left = left
        self.top = top
        self.time = time.time()
        self.opacity = opacity
        self.size = size

    def start(self):
        self.time = time.time()

    def elapsed(self):
        return timedelta(seconds=int(time.time() - self.time))

    def draw(self):
        # https://www.geeksforgeeks.org/python-datetime-timedelta-function/
        # https://www.geeksforgeeks.org/format-a-number-width-in-python/
        e = self.elapsed()
        text = f'{self.text}: {e.seconds//60:02d}:{e.seconds%60:02d}'
        drawLabel(text, self.left, self.top, size=self.size, opacity=self.opacity)

class LabelButton:
    def __init__(self, text, l, t, color, border, borderWidth=2, opacity=60,size=60):
        self.text = text
        self.l = l
        self.t = t
        self.color = color
        self.border = border
        self.borderWidth = borderWidth
        self.opacity = opacity
        self.isSelected = False
        self.isChecked = False
        self.size = size

    def mousePress(self, mouseX, mouseY):
        if self.mouseOver(mouseX, mouseY):
            self.isChecked = not self.isChecked
        else:
            self.isChecked = False
        return self.isChecked

    def mouseOver(self, mouseX, mouseY):
        # calculate the positions from center for left, right, top, bottom
        # x is the total length of the text on screen
        offsetX = len(self.text) * self.size / 2
        offsetY = self.size

        if (self.l - offsetX <= mouseX <= self.l + offsetX) and (self.t - offsetY <= mouseY <= self.t + offsetY):
            self.isSelected = True
        else:
            self.isSelected = False
        return self.isSelected

    def draw(self):
        text = self.text
        opacity = self.opacity
        left = self.l
        if self.isChecked:
            text = f"[{self.text}]"
            opacity = 100
            left -= 1
        elif self.isSelected:
            text = f"[{self.text}]"
            left -= 1

        drawLabel(text, left, self.t, font='cinzel',
                  size=self.size, fill=self.color, border=self.border, borderWidth=self.borderWidth,
                  opacity=opacity)

class Checkbox:
    def __init__(self, text, l, t, color, border, borderWidth=0, opacity=60, size=17):
        self.text = text
        self.l = l
        self.t = t
        self.color = color
        self.border = border
        self.borderWidth = borderWidth
        self.opacity = opacity
        self.isChecked = False
        self.isSelected = False
        self.size = size

    def mousePress(self, mouseX, mouseY):
       if self.mouseOver(mouseX, mouseY):
           self.isChecked = not self.isChecked
      # return self.isChecked (this is incorrect)

    def mouseOver(self, mouseX, mouseY):
        # calculate the positions from center for left, right, top, bottom
        # x is the total length of the text on screen
        offsetX = len(self.text) * self.size / 2
        offsetY = self.size

        if (self.l - offsetX <= mouseX <= self.l + offsetX) and (self.t - offsetY <= mouseY <= self.t + offsetY):
            self.isSelected = True
        else:
            self.isSelected = False
        return self.isSelected

    def draw(self):
        opacity = self.opacity
        text = f'[  ] {self.text}'
        if self.isChecked:
            if self.isSelected:
                opacity = 100
            text = f'[x] {self.text}'
        elif self.isSelected:
            opacity = 100

        drawLabel(text, self.l, self.t, font='cinzel',
                  size=self.size, fill=self.color, border=self.border, borderWidth=self.borderWidth,
                  opacity=opacity)


def onKeyUpdateButtons(buttons, up=True):
    p = -1

    for i in range(len(buttons)):
        if buttons[i].isSelected:
            p = i
            break

    if p == -1:
        buttons[0].isSelected = True
        return

    buttons[p].isSelected = False

    if not up:
        p += 1
        if p >= len(buttons):
            p = 0
    else:
        p -= 1
        if p < 0:
            p = len(buttons) - 1

    buttons[p].isSelected = True

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
     