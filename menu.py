from cmu_graphics import *
from button import *

class MenuScreen:
    def __init__(self):
        # initialize the buttons we'll need on the menu
        self.buttons = [
            LabelButton('play', 270, 230, 'black', 'forestgreen'),
            LabelButton('help', 270, 330, 'black', 'forestgreen')
            ]
        self.selected = 0
        

def menu_onAppStart(app):
    app.menuScreen = MenuScreen()
    # initialize a selected button (may want to change)
    app.menuScreen.buttons[0].isSelected = True

def menu_onKeyPress(app, key):
    if key == 'up':
        onKeyUpdateButtons(app.menuScreen.buttons, True)
    elif key == 'down':
        onKeyUpdateButtons(app.menuScreen.buttons, False)
    elif key == 'enter':
        for button in app.menuScreen.buttons:
            if button.isSelected:
                app.screenSwitchSound.play()
                setActiveScreen(button.text)

def menu_onMouseMove(app, mouseX, mouseY):
    for button in app.menuScreen.buttons:
        button.mouseOver(mouseX, mouseY)

def menu_onMousePress(app, mouseX, mouseY):
    for button in app.menuScreen.buttons:
        if button.mouseOver(mouseX, mouseY):
            app.screenSwitchSound.play()
            setActiveScreen(button.text)

def menu_redrawAll(app):
    # draw background and Sudoku logo
    drawImage('./media/splash.png', 0, 0, opacity=50)
    drawLabel('Sudoku', 260, 100, font='cinzel', size=80, fill='forestgreen',
                border='lightgray', borderWidth=2, opacity=60)
    # draw buttons
    for button in app.menuScreen.buttons:
        button.draw()
