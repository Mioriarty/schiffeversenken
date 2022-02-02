import pygame
import numpy as np

class Input:

    __currentEvents = {}


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