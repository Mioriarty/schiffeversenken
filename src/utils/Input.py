import pygame
import numpy as np

class Input:
    """
    Static class that manages all kinds of pygame events and mouse inputs.

    (Except for the QUIT event)
    """

    __currentEvents = {}

    GAME_LAYER = 0
    ENDGAME_SIGN_LAYER = 1
    SETTINGS_LAYER = 2

    __crntInputLayer = GAME_LAYER
    __requestedInputLayer = GAME_LAYER

    # input layer related methods
    @staticmethod
    def setInputLayer(inputLayer : int, resetCursor : bool = True) -> None:
        """
        Sets the input layer inthe end of that frame.

        The input layer is a global value that should be used to automatically disable all buttons etc that are not on the soma input layer as the current layer.

        Predefined values are: GAME_LAYER, ENDGAME_SIGN_LAYER, SETTINGS_LAYER

        Args:
            inputLayer (int): The requested input layer.
            resetCursor (bool, optional): Determines whther the mouse curser should be changed to the stadart curser. Defaults to True.
        """
        Input.__requestedInputLayer = inputLayer
        if resetCursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    @staticmethod
    def checkInputLayer(requestedLayer : int) -> bool:
        """
        Checks for an certain value of the input layer.

        Args:
            requestedLayer (int): The layer checked against.

        Returns:
            bool: If the current layer is equal to the requested layer.
        """
        return Input.__crntInputLayer == requestedLayer


    # handled by main
    @staticmethod
    def clearEvents() -> None:
        """
        Clears all stored events.

        Prepration for the next frame.
        """
        Input.__crntInputLayer = Input.__requestedInputLayer
        Input.__currentEvents = {}
    
    @staticmethod
    def enterEvent(event : pygame.event.Event) -> None:
        """
        Input a fetched event from pygame.

        Args:
            event (pygame.event.Event): The evemt that got fetched from pygame.
        """
        Input.__currentEvents[event.type] = event
    

    # for all components
    @staticmethod
    def hasEvent(type : int) -> bool:
        """
        Returns whether the event has occured during the last frame.

        Args:
            type (int): The requested event type. Look into pygame events for details.

        Returns:
            bool: If that event occured during the last frame.
        """
        return type in Input.__currentEvents
    
    @staticmethod
    def getEvent(type : int) -> pygame.event.Event:
        """
        Fetches an epygame event of a specified type.

        Args:
            type (int): The requested event type. Look into pygame events for details.

        Returns:
            pygame.event.Event | None: The event of the specified type. If this event has not happened during the last frame it will return None.
        """
        return Input.__currentEvents[type] if type in Input.__currentEvents else None
    
    @staticmethod
    def getMousePos() -> np.ndarray:
        """
        Returns the current mouse position.

        Returns:
            np.ndarray: The current mouse position.
        """
        return np.array(pygame.mouse.get_pos())