import pygame
import numpy as np

class Input:

    __currentEvents = {}

    GAME_LAYER = 0
    ENDGAME_SIGN_LAYER = 1
    SETTINGS_LAYER = 2

    __crntInputLayer = GAME_LAYER

    @staticmethod
    def setInputLayer(inputLayer : int, resetCursor : bool = True) -> None:
        Input.__crntInputLayer = inputLayer
        if resetCursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    @staticmethod
    def checkInputLayer(requestedLayer : int) -> bool:
        return Input.__crntInputLayer == requestedLayer


    # handled by main
    @staticmethod
    def clearEvents() -> None:
        Input.__currentEvents = {}
    
    @staticmethod
    def enterEvent(event : pygame.event.Event) -> None:
        Input.__currentEvents[event.type] = event
    

    # for all components
    @staticmethod
    def hasEvent(type : int) -> bool:
        return type in Input.__currentEvents
    
    @staticmethod
    def getEvent(type : int) -> pygame.event.Event:
        return Input.__currentEvents[type] if type in Input.__currentEvents else None
    
    @staticmethod
    def getMousePos() -> np.ndarray:
        return np.array(pygame.mouse.get_pos())