from cmu_graphics import *
from button import *

class HelpScreen:
    def __init__(self):
        self.buttons = [LabelButton('back', 50, 520, 'black', 'black', size = 20)]

def help_onAppStart(app):
    app.helpScreen = HelpScreen()

def help_onMouseMove(app, mouseX, mouseY):
    for button in app.helpScreen.buttons:
        button.mouseOver(mouseX, mouseY)

def help_onKeyPress(app, key):
    if key == 'up':
        onKeyUpdateButtons(app.helpScreen.buttons, True)
    elif key == 'down':
        onKeyUpdateButtons(app.helpScreen.buttons, False)
    elif key == 'enter':
        for button in app.helpScreen.buttons:
            if button.isSelected:
                app.screenSwitchSound.play()
                setActiveScreen('menu')

def help_onMousePress(app, mouseX, mouseY):
    for button in app.helpScreen.buttons:
        if button.mouseOver(mouseX, mouseY):
            app.screenSwitchSound.play()
            setActiveScreen('menu')

def help_readFile(filename):
    with open(filename, "rt") as f:
        return f.read()

def help_drawHelp(path, left, top, width, height):
    help = help_readFile(path)

    lineLength = 54
    drawRect(left, top, width, height, fill='white', opacity = 60)

    centerX = (left + width)/2 + 20
    centerY = top + 60

    lines = help.split('\n')
    for i in range(len(lines)):
        # https://www.geeksforgeeks.org/python-padding-a-string-upto-fixed-length/
        line = lines[i].ljust(lineLength)
        # use monospace because the letters are of equal size, otherwise
        # the text will be off centered
        # https://en.wikipedia.org/wiki/Monospaced_font#:~:text=A%20monospaced%20font%2C%20also%20called,and%20spacings%20have%20different%20widths.
        drawLabel(line, centerX, centerY + i*30, size=13,font='monospace')

def help_redrawAll(app):
    drawImage('./media/splash.png', 0, 0, opacity=50)
    for button in app.helpScreen.buttons:
        button.draw()
    help_drawHelp('help.txt', 50, 98, 480, 380 ) #290, 120)
    drawLabel('Sudoku', 260, 100, font='cinzel', size=80, fill='forestgreen',
        border='lightgray', borderWidth=2, opacity=60)

