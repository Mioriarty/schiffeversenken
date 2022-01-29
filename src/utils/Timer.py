from typing import Callable
from utils.InstanceRegistryMetaClass import InstanceRegistryMetaClass

class Timer(metaclass = InstanceRegistryMetaClass):

    def __init__(self, duration : float, callback : Callable[[], None] = None, loop : bool = False):
        self.__duration = duration
        self.__elapsedTime = 0.
        self.__loop = loop
        self.__isRunning = False
        self.__callback = callback

    def start(self) -> None:
        self.__isRunning = True
    
    def setDuration(self, duration : float) -> None:
        self.__duration = duration
    
    def update(self, dt : float) -> None:
        if self.__isRunning:
            self.__elapsedTime += dt

            if self.__elapsedTime >= self.__duration:
                if self.__callback is not None:
                    self.__callback()
                
                self.__elapsedTime = 0.
                
                if not self.__loop:
                    self.__isRunning = False


    @staticmethod
    def updateAll(dt : float) -> None:
        for a in Timer._instances:
            a.update(dt)