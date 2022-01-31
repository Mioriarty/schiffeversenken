import pygame
from components.Component import Component
from scenes.GameScene import GameScene
from scenes.LogoScene import LogoScene
from scenes.Scene import SceneManager
from scenes.TestScene import TestScene
from scenes.menu.MenuScene import MenuScene
from utils.Animator import Animator
from utils.Timer import Timer
from utils.Images import Images
from utils.Sounds import Sounds

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WINDOW_TITLE = "Schiffe versenken"
FRAME_RATE = 120


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, 16)
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.event.set_allowed([ pygame.QUIT ])

    clock = pygame.time.Clock()

    shouldRun = True

    Images.loadAll()
    Sounds.loadAll()

    SceneManager.requestloadScene(GameScene)

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

        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shouldRun = False

        pygame.display.update()
    
    pygame.quit()



if __name__ == "__main__":
    main()