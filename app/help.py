from cmu_graphics import *
from button import *

class HelpScreen:
    def __init__(self):
        self.buttons = [Button('back', 40, 520, 80, 50, shape='oval')]

def help_onAppStart(app):
    app.helpScreen = HelpScreen()

def help_onMouseMove(app, mouseX, mouseY):
    for button in app.helpScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'crimson'

def help_onMousePress(app, mouseX, mouseY):
    for button in app.helpScreen.buttons:
        button.color = 'white'
        if button.mouseOver(mouseX, mouseY):
            button.color = 'crimson'
            setActiveScreen('menu')

def help_redrawAll(app):
    drawLabel('on this screen the readme file will be displayed', 200, 200, 
              size = 16)
    
    for button in app.helpScreen.buttons:
        button.draw()

    # # for back button
    # drawCircle(app.backcx, app.backcy, app.r, 
    #            fill = app.backCircleColor, border = 'black', borderWidth = 5)
    # drawLabel('Back', app.backcx, app.backcy, size = 20)

