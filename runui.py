from cmu_graphics import *
from splash import *
from menu import *
from help import *
from play import *
from game import *
from boards.loader import FileBoardLoader 
from boards.hints import *

def onAppStart(app):
    print('app starting')
    # load the boards
    app.boardLoader = FileBoardLoader("./boards/files")
    app.screenSwitchSound = Sound('https://cdn.pixabay.com/download/audio/2022/03/15/audio_bc8824d8ca.mp3?filename=door-close-79921.mp3')

def onAppStop(app):
    print('app stopping') 

def main():
    # start the program with our splash screen
    # background image was generated using https://www.canva.com/ai-image-generator/
    runAppWithScreens(initialScreen = 'splash', width = 520, height = 570)

main()