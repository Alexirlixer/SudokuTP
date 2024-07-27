from cmu_graphics import *
from splash import *
from menu import *
from help import *
from play import *
from game import *

def onAppStart(app):
    print('app starting')

def onAppStop(app):
    print('app stopping')

def main():
    runAppWithScreens(initialScreen = 'splash', width = 400, height = 600)

main()