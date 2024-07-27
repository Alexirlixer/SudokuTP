from cmu_graphics import *

def help_onAppStart(app):
    app.backcx = 80
    app.backcy = 520
    app.r = 50
    app.backCircleColor = 'white'


def help_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def help_onMouseMove(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.backcx, app.backcy) <= app.r:
        app.backCircleColor = 'red'
    else:
        app.backCircleColor = 'white'

def help_onMousePress(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.backcx, app.backcy) <= app.r:
        setActiveScreen('menu')

def help_redrawAll(app):
    drawLabel('on this screen the readme file will be displayed', 200, 200, size = 16)
    drawCircle(app.backcx, app.backcy, app.r, 
               fill = app.backCircleColor, border = 'black', borderWidth = 5)
    drawLabel('Back', app.backcx, app.backcy, size = 20)

