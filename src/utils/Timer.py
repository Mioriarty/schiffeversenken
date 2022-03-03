from typing import Callable
from utils.InstanceRegistryMetaClass import InstanceRegistryMetaClass

class Timer(metaclass = InstanceRegistryMetaClass):
    """
    Represents a timer that always fires after a certain pereod of time.
    """

    def __init__(self, duration : float, callback : Callable[[], None] = None, loop : bool = False):
        """
        The constructor of the Timer class.

        Args:
            duration (float): The duration until the timer fires in seconds.
            callback (Callable[[], None], optional): The callback that gets called when the timer reached the end. Defaults to None.
            loop (bool, optional): Determines whther the timner should start agin after it reached the end. Defaults to False.
        """
        self.__duration = duration
        self.__elapsedTime = 0.
        self.__loop = loop
        self.__isRunning = False
        self.__callback = callback

    def start(self) -> None:
        """
        Starts the timer.
        """
        self.__isRunning = True
    
    def setDuration(self, duration : float) -> None:
        """
        Sets the duration until the timer fires in seconds.

        Args:
            duration (float): The new duartion until the timer fires in seconds.
        """
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
        """
        Updates all timers kept rack by the registry.

        Args:
            dt (float): Time that has past since the last frame in seconds.
        """
        for a in Timer._instances:
            a.update(dt)