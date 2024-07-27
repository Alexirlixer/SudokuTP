from cmu_graphics import *

def play_onAppStart(app):
    # for all of the difficulty selectors
    app.boxLeft = 150
    app.easyTop = 275
    app.mediumTop = 350
    app.hardTop = 425
    app.evilTop = 500
    app.boxWidth = 100
    app.boxHeight = 50
    app.easyBoxColor = 'white'
    app.mediumBoxColor = 'white'
    app.hardBoxColor = 'white'
    app.evilBoxColor = 'white'
    # for back button
    app.backcx = 80
    app.backcy = 520
    app.r = 50
    app.backCircleColor = 'white'

def play_onMouseMove(app, mouseX, mouseY):
    # for easy
    if ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth)
        and (app.easyTop <= mouseY <= app.easyTop + app.boxHeight)):
        app.easyBoxColor = 'mediumSeaGreen'
    # for medium
    elif ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth) 
          and (app.mediumTop <= mouseY <= app.mediumTop + app.boxHeight)):
        app.mediumBoxColor = 'mediumSeaGreen'
    # for hard
    elif ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth) and 
          (app.hardTop <= mouseY <= app.hardTop + app.boxHeight)):
        app.hardBoxColor = 'mediumSeaGreen'
    # for evil
    elif ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth) and
          (app.evilTop <= mouseY <= app.evilTop + app.boxHeight)):
        app.evilBoxColor = 'mediumSeaGreen'
    # for back button
    elif distance(mouseX, mouseY, app.backcx, app.backcy) <= app.r:
        app.backCircleColor = 'red'
    # otherwise everything should be white
    else:
        app.easyBoxColor = 'white'
        app.mediumBoxColor = 'white'
        app.hardBoxColor = 'white'
        app.evilBoxColor = 'white'
        app.backCircleColor = 'white'

def play_onMousePress(app, mouseX, mouseY):
    # for easy
    if ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth)
        and (app.easyTop <= mouseY <= app.easyTop + app.boxHeight)):
        # setActiveScreen('game') (on easy mode)
        pass
    # for medium
    elif ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth) 
          and (app.mediumTop <= mouseY <= app.mediumTop + app.boxHeight)):
        # setActiveScreen('game') (on medium mode)
        pass
    # for hard
    elif ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth) and 
          (app.hardTop <= mouseY <= app.hardTop + app.boxHeight)):
        # setActiveScreen('game') (on hard mode)
        pass
    # for evil
    elif ((app.boxLeft <= mouseX <= app.boxLeft + app.boxWidth) and
          (app.evilTop <= mouseY <= app.evilTop + app.boxHeight)):
        # setActiveScreen('game') (on evil mode)
        pass
    # for back button
    elif distance(mouseX, mouseY, app.backcx, app.backcy) <= app.r:
        setActiveScreen('menu')

def play_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def play_redrawAll(app):
    # maybe get rid of this rect code, it just draws a border around the screen
    drawRect(0, 0, 400, 600, fill = None, border = 'black', borderWidth = 10)
    drawLabel('Sudoku', 200, 100, size = 85)
    drawLabel('Select Difficulty', 200, 200, size = 30)
    # for easy
    drawRect(app.boxLeft, app.easyTop, app.boxWidth, app.boxHeight, 
             fill = app.easyBoxColor, border = 'black', borderWidth = 2)
    drawLabel('Easy', app.boxLeft + app.boxWidth/2, 
              app.easyTop + app.boxHeight/2, size = 20)
    # for medium
    drawRect(app.boxLeft, app.mediumTop, app.boxWidth, app.boxHeight, 
             fill = app.mediumBoxColor, border = 'black', borderWidth = 2)
    drawLabel('Medium', app.boxLeft + app.boxWidth/2, 
              app.mediumTop + app.boxHeight/2, size = 20)
    # for hard
    drawRect(app.boxLeft, app.hardTop, app.boxWidth, app.boxHeight, 
             fill = app.hardBoxColor, border = 'black', borderWidth = 2)
    drawLabel('Hard', app.boxLeft + app.boxWidth/2, 
              app.hardTop + app.boxHeight/2, size = 20)
    # for evil
    drawRect(app.boxLeft, app.evilTop, app.boxWidth, app.boxHeight, 
             fill = app.evilBoxColor, border = 'black', borderWidth = 2)
    drawLabel('Evil', app.boxLeft + app.boxWidth/2, 
              app.evilTop + app.boxHeight/2, size = 20)
    # for back button
    drawCircle(app.backcx, app.backcy, app.r, 
               fill = app.backCircleColor, border = 'black', borderWidth = 5)
    drawLabel('Back', app.backcx, app.backcy, size = 20)

