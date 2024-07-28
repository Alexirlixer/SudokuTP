from cmu_graphics import *
from button import *

class MenuScreen:
    def __init__(self):
        self.buttons = [Button('play', 105, 235, 190, 130, shape='oval'),
                        Button('help', 105, 395, 190, 130, shape='oval')]
        

def menu_onAppStart(app):
    app.menuScreen = MenuScreen()

def menu_onKeyPress(app, key):
    if key == 'n':
        setActiveScreen('splash')

def menu_onMouseMove(app, mouseX, mouseY):
    for button in app.menuScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'mediumSeaGreen'

def menu_onMousePress(app, mouseX, mouseY):
     for button in app.menuScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'mediumSeaGreen'
            setActiveScreen(button.name)

def menu_redrawAll(app):
    drawRect(0, 0, 400, 600, fill = None, border = 'black', borderWidth = 10)
    drawLabel('Sudoku', 200, 100, size = 85)

    for button in app.menuScreen.buttons:
        button.draw()
