import utils
import pygame


class Component(metaclass = utils.InstanceRegistryMetaClass):

    def __init__(self, transform : utils.Transform):
        self.transform = transform

    def update(self, dt : float) -> None:
        pass

    def draw(self, screen : pygame.Surface) -> None:
        pass

    @staticmethod
    def updateAll(dt : float) -> None:
        for c in Component._instances:
            c.update(dt)

    @staticmethod
    def drawAll(screen : pygame.Surface) -> None:
        for c in Component._instances:
            c.draw(screen)
