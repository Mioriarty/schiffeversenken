from typing import Callable
from components.Component import Component
from utils import Sounds, Transform
import pygame
import numpy as np

from utils.Input import Input


class AbstractButton(Component):
    """
    Represents a rect with an arbetrary Transform, that can be clicked.

    For behavoir, derive from it and overwrite the on-... methods.
    """

    def __init__(self, width : float, height : float, inputLayer : int, transform: Transform = None):
        """
        Constructor of the AbstractButton class.

        Args:
            width (float): Width of the clickable area.
            height (float): Height of the clickable area.
            inputLayer (int): The input layer of the AbstractButton. If that layer doesn't match the current input layer (see Input class), the button won't be clickable.
            transform (Transform, optional): The Transform of the component. Defaults to None.
        """
        super().__init__(transform)
        self.width = width
        self.height = height
        self.inputLayer = inputLayer

        self.__enabled = True
        self.__hovering = False
        self.__pressed = False
        self.__hoverCursor = pygame.SYSTEM_CURSOR_HAND

        self.__onClickEvent : Callable[[], None] = None

    def update(self, dt : float) -> None:
        if self.__enabled and Input.checkInputLayer(self.inputLayer):
            relativeMousePos = np.absolute(self.transform.applyInv(Input.getMousePos()))
            hovering = 2 * relativeMousePos[0] <= self.width and 2 * relativeMousePos[1] <= self.height
            
            if hovering and not self.__hovering:
                pygame.mouse.set_cursor(self.__hoverCursor)
                self.onMouseEnter()
            elif not hovering and self.__hovering:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if self.__pressed:
                    self.onPressCancel()
                    self.__pressed = False
                self.onMouseExit()

            self.__hovering = hovering
            
            if hovering:
                clicked = Input.hasEvent(pygame.MOUSEBUTTONDOWN) and Input.getEvent(pygame.MOUSEBUTTONDOWN).button == 1

                if clicked:
                    self.onMouseDown()
                    self.__pressed = True
                elif self.__pressed:
                    released = Input.hasEvent(pygame.MOUSEBUTTONUP) and Input.getEvent(pygame.MOUSEBUTTONUP).button == 1
                    if released:
                        self.onMouseUp()
                        
                        # actually call the onclick event
                        if self.__onClickEvent is not None:
                            Sounds.playSoundEffect("click")
                            self.__onClickEvent()
                        self.__pressed = False
                    
    
    def setOnClickEvent(self, clickEvent : Callable[[], None]) -> None:
        """
        Sets a callback function that gets called when the button is pressed.

        Args:
            clickEvent (Callable[[], None]): The callback function that gets called when the button is pressed.
        """
        self.__onClickEvent = clickEvent

    def addOnClickEvent(self, clickEvent : Callable[[], None]) -> None:
        """
        Adds another callback function that gets called when the button is pressed.

        Can also be called without having called setOnClickEvent before.

        Args:
            clickEvent (Callable[[], None]): The new callback function that gets called when the button is pressed.
        """
        if self.__onClickEvent is None:
            self.__onClickEvent = clickEvent
        else:
            oldEvent = self.__onClickEvent
            def newEvent():
                oldEvent()
                clickEvent()
            self.__onClickEvent = newEvent
    
    def enable(self) -> None:
        """
        Enables the button.

        The button will be clickable again if the current input layer (see Input class) matches its input layer.
        """
        self.__enabled = True

        self.onEnable()
    
    def disable(self) -> None:
        """
        Disables the button.

        The button won't be clickable anymore.
        """
        if self.__hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        self.__enabled = False
        self.__pressed = False
        self.__hovering = False

        self.onDisable()
        


    def onMouseEnter(self) -> None:
        """
        Gets called when the mouse enters the area of the abstract button.

        It will also be called when the mouse button is hold when that happens.
        """
        pass

    def onMouseExit(self) -> None:
        """
        Gets called when the mouse exits the area of the abtract button.

        It won't be called when the mouse button is hold when that happens.
        """
        pass

    def onMouseDown(self) -> None:
        """
        Gets called when the mouse button gets pressed down while the curser is in the area of the abstract button.
        """
        pass

    def onMouseUp(self) -> None:
        """
        Gets called when the mouse button is released while the curser is in the area of the abstract button.
        """
        pass

    def onPressCancel(self) -> None:
        """
        Gets called when the mouse button is hold down and the curser exits the area of the abstract button.
        """
        pass

    def onEnable(self) -> None:
        """
        Gets called when enable() is called.
        """
        pass

    def onDisable(self) -> None:
        """
        Gets called when disable() is called.
        """
        pass
