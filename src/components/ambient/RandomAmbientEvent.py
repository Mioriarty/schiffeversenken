import pygame, random
from components.ambient.Diashow import Diashow
from utils.Animator import Animator
from utils.Timer import Timer
from utils.Transform import Transform


class RandomAmbientEvent(Diashow):

    def __init__(self, images: list[str | pygame.Surface], imageDuration: float, appearanceRect : pygame.Rect, waitSpan : tuple[float], transform: Transform = None):
        super().__init__(images, imageDuration, transform)
        self.animation.stop()
        self.animation.setRepeatMode(Animator.STOP)
        self.animation.setEndCallback(self.startNextCycle)
        self.__timer = Timer(0, self.animation.play)
        self.__apppearanceRect = appearanceRect
        self.__waitSpan = waitSpan

        self.startNextCycle()
    
    def startNextCycle(self) -> None:
        print("Hi")
        self.__timer.setDuration(random.random() * (self.__waitSpan[1] - self.__waitSpan[0]) + self.__waitSpan[0])
        self.__timer.start()
        self.transform.setRelPosition((
            self.__apppearanceRect.x + self.__apppearanceRect.width * random.random(),
            self.__apppearanceRect.y + self.__apppearanceRect.height * random.random()
        ))

    
    def draw(self, screen: pygame.Surface) -> None:
        if self.animation.isRunning():
            super().draw(screen)


class Shark(RandomAmbientEvent):

    def __init__(self, imageDuration: float, appearanceRect: pygame.Rect, waitSpan: tuple[float], transform: Transform = None):
        super().__init__([ "ambient.shark1", "ambient.shark2", "ambient.shark3", "ambient.shark4", "ambient.shark5", "ambient.shark6", "ambient.shark7", "ambient.shark8" ], imageDuration, appearanceRect, waitSpan, transform)