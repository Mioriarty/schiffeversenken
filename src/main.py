import pygame
from components.Component import Component
from scenes.LogoScene import LogoScene
from scenes.Scene import SceneManager
from scenes.TestScene import TestScene
from utils.Animator import Animator
from utils.Images import Images
from utils.Sounds import Sounds

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WINDOW_TITLE = "Schiffe versenken"
CLEAR_COLOR = (0, 0, 0)
FRAME_RATE = 75

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    shouldRun = True

    Images.loadAll()
    Sounds.loadAll()

    SceneManager.requestloadScene(LogoScene)
    

    while shouldRun:
        dt = clock.tick(FRAME_RATE) / 1000
        screen.fill(CLEAR_COLOR)

        # load new scene if it was requested
        SceneManager.loadNewSceneIfRequested()

        # updates
        Animator.updateAll(dt)
        Component.updateAll(dt)

        # draw
        SceneManager.drawAll(screen)

        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shouldRun = False

        pygame.display.flip()
    
    pygame.quit()



if __name__ == "__main__":
    main()