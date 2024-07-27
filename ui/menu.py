from cmu_graphics import *

def menu_onAppStart(app):
    # oval variables
    # app.playOvalcx = 200
    # app.playOvalcy = 300
    # app.helpOvalcx = 200
    # app.helpOvalcy = 450
    # app.ovalWidth = 200
    # app.ovalHeight = 100
    # app.playOvalColor = 'white'
    # app.helpOvalColor = 'white'
    app.r = 65
    app.playcx = 200
    app.playcy = 300
    app.helpcx = 200
    app.helpcy = 450
    app.playCircleColor = 'white'
    app.helpCircleColor = 'white'


def menu_onKeyPress(app, key):
    if key == 'n':
        setActiveScreen('splash')

def menu_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Learned about this calculation from https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
# def menu_ovalIntersection(x1, y1, x2, y2, rWidth, rHeight):
#     # where x1 is the mouseX and x2 is the cx of the oval (same goes for y1 and y2)
#     return (((x1 - x2)**2)/(rWidth)**2) + (((y1 - y2)**2)/(rHeight)**2) <= 0.4

def menu_onMouseMove(app, mouseX, mouseY):
    # This is the code to check for the intersection with the ovals
    # if menu_ovalIntersection(mouseX, mouseY, app.playOvalcx, app.playOvalcy, 
    #                          app.ovalWidth, app.ovalHeight):
    #     app.playOvalColor = 'mediumSeaGreen'
    # # elif menu_ovalIntersection(mouseX, mouseY, app.helpOvalcx, app.helpOvalcy,
    # #                          app.ovalWidth, app.ovalHeight):
    # #     app.helpOvalColor = 'mediumSeaGreen'
    # else:
    #     app.playOvalColor = 'white'
    #     app.helpOvalColor = 'white'
    if distance(mouseX, mouseY, app.playcx, app.playcy) <= app.r:
        app.playCircleColor = 'mediumSeaGreen'
    elif distance(mouseX, mouseY, app.helpcx, app.helpcy) <= app.r:
        app.helpCircleColor = 'mediumSeaGreen'
    else:
        app.playCircleColor = 'white'
        app.helpCircleColor = 'white'

def menu_onMousePress(app, mouseX, mouseY):
    if distance(mouseX, mouseY, app.playcx, app.playcy) <= app.r:
        setActiveScreen('play')
        
    elif distance(mouseX, mouseY, app.helpcx, app.helpcy) <= app.r:
        setActiveScreen('help')

def menu_redrawAll(app):
    drawRect(0, 0, 400, 600, fill = None, border = 'black', borderWidth = 10)
    drawLabel('Sudoku', 200, 100, size = 85)

    # for oval
    # drawOval(app.playOvalcx, app.playOvalcy, app.ovalWidth,
    #           app.ovalHeight, fill = app.playOvalColor, 
    #           border = 'black', borderWidth = 2)

    drawCircle(app.playcx, app.playcy, app.r, 
               fill = app.playCircleColor, border = 'black', 
               borderWidth = 5)
    drawLabel('Play', 200, 300, size = 30)

    # for oval
    # drawOval(app.helpOvalcx, app.helpOvalcy, app.ovalWidth, 
    #          app.ovalHeight, fill = app.helpOvalColor,
    #            border = 'black', borderWidth = 2)
    drawCircle(app.helpcx, app.helpcy, app.r, 
               fill = app.helpCircleColor, border = 'black', 
               borderWidth = 5)
    drawLabel('Help', 200, 450, size = 30)

