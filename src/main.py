# version check
import sys
if sys.version_info.major < 3 or sys.version_info.minor < 10:
    raise Exception("Must be using Python 3.10 or higher")

import pygame
from components.Component import Component
from scenes.LogoScene import LogoScene
from scenes.Scene import SceneManager
from utils.Animator import Animator
from utils.Input import Input
from utils.Timer import Timer
from utils.Images import Images
from utils.Sounds import Sounds

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 798
WINDOW_TITLE = "Schiffe versenken"
FRAME_RATE = 120


def main():
    # Initiate pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, 16)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    shouldRun = True

    # Load recources
    Images.loadAll()
    Sounds.loadAll()

    # load first scene
    SceneManager.requestloadScene(LogoScene)

    # main game loop
    while shouldRun:
        # load new scene if it was requested
        SceneManager.loadNewSceneIfRequested()

        dt = clock.tick(FRAME_RATE) / 1000
        screen.fill(SceneManager.getClearColor())

        # updates
        Timer.updateAll(dt)
        Animator.updateAll(dt)
        Component.updateAll(dt)

        # draw
        SceneManager.drawAll(screen)

        # load requested components
        SceneManager.createRequestedComponents()

        # catch events
        Input.clearEvents()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shouldRun = False
            else:
                Input.enterEvent(event)

        pygame.display.update()
    
    pygame.quit()



if __name__ == "__main__":
    main()