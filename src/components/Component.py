import utils
import pygame


class Component(metaclass = utils.InstanceRegistryMetaClass):

    def __init__(self, transform : utils.Transform):
        self.transform : utils.Transform = utils.Transform.fromTransform(transform)

    def update(self, dt : float) -> None:
        pass

    def draw(self, screen : pygame.Surface) -> None:
        pass

    @staticmethod
    def updateAll(dt : float) -> None:
        for c in Component._instances:
            c.update(dt)