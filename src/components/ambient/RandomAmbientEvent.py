import pygame, random
from components.ambient.Diashow import Diashow
from utils.Animator import Animator
from utils.Timer import Timer
from utils.Transform import Transform


class RandomAmbientEvent(Diashow):
    """
    Simple Diashows that appear randomly in a rectangle with randomized waiting times.
    """

    def __init__(self, images: list[str | pygame.Surface], imageDuration: float, appearanceRect : pygame.Rect, waitSpan : tuple[float], transform: Transform = None):
        """
        Constrcutor of the RandomAmbientEvent class.

        Args:
            images (list[str | pygame.Surface]): The images that should be shown after another.
            imageDuration (float): The duration of one image.
            appearanceRect (pygame.Rect): Determines in waht rect on the screen the event can appear.
            waitSpan (tuple[float]): Determines minimum and maximum waiting times between events.
            transform (Transform, optional): The tranform of the component. Defaults to None.
        """
        super().__init__(images, imageDuration, False, transform)
        self.animation.stop()
        self.animation.setEndCallback(self.startNextCycle)
        self.__timer = Timer(0, self.animation.replay)
        self.__apppearanceRect = appearanceRect
        self.__waitSpan = waitSpan

        self.startNextCycle()
    
    def startNextCycle(self) -> None:
        """
        Callback that gets called when the event ended.

        It will start a timer to wait until the next eppearance.
        """
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
    """
    Represents a shark that can randomly appear on the screen.

    It is a basic implementation of the RandomAmbientEvent class.
    """

    def __init__(self, imageDuration: float, appearanceRect: pygame.Rect, waitSpan: tuple[float], transform: Transform = None):
        super().__init__([ "ambient.shark1", "ambient.shark2", "ambient.shark3", "ambient.shark4", "ambient.shark5", "ambient.shark6", "ambient.shark7", "ambient.shark8" ], imageDuration, appearanceRect, waitSpan, transform)