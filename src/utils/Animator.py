from utils.InstanceRegistryMetaClass import InstanceRegistryMetaClass
from typing import Callable
import math

class Animator(metaclass = InstanceRegistryMetaClass):

    STOP    = 0
    PAUSE   = 1
    RESTART = 2
    REVERSE = 3

    def __init__(self, equation, duration : float):
        self.__equation : Callable[[float], any] = equation
        self.__duration : float                  = duration
        self.__elapsedTime : float               = 0
        self.__timeScale : float                 = 1
        self.__isRunning : bool                  = False
        self.__repeatMode : int                  = Animator.PAUSE
        self.__hook : Callable[[any], None]      = None
        self.__endCallback : Callable[[], None ] = None

    def play(self) -> None:
        self.__isRunning = True
    
    def replay(self) -> None:
        self.stop()
        self.play()

    def update(self, dt : float) -> None:
        if self.__isRunning:
            self.__elapsedTime += dt * self.__timeScale

            if self.__elapsedTime > self.__duration:
                self.__elapsedTime = self.__duration

                if self.__repeatMode == Animator.STOP:
                    self.stop()
                elif self.__repeatMode == Animator.PAUSE:
                    self.pause()
                elif self.__repeatMode == Animator.RESTART:
                    self.__elapsedTime = 0
                elif self.__repeatMode == Animator.REVERSE:
                    self.__timeScale *= -1
                
                if self.__endCallback != None:
                    self.__endCallback()
            
            elif self.__elapsedTime < 0:
                self.__elapsedTime = 0

                if self.__repeatMode == Animator.STOP:
                    self.stop()
                elif self.__repeatMode == Animator.PAUSE:
                    self.pause()
                elif self.__repeatMode == Animator.RESTART:
                    self.__elapsedTime = self.__duration
                elif self.__repeatMode == Animator.REVERSE:
                    self.__timeScale *= -1
                
                if self.__endCallback != None:
                    self.__endCallback()
            
            if self.__hook != None:
                self.__hook(self.get())

                

    def get(self) -> any:
        return self.__equation(self.__elapsedTime)
    
    def pause(self) -> None:
        self.__isRunning = False
    
    def stop(self) -> None:
        self.__isRunning = False
        self.__elapsedTime = 0
        self.__timeScale = abs(self.__timeScale)
    
    def skipToEnd(self) -> None:
        self.__elapsedTime = self.__duration
        self.update(0)
    
    def concat(self, other : 'Animator') -> 'Animator':
        equation = lambda t : self.__equation(t) if t < self.__duration else other.__equation(t - self.__duration)
        return Animator(equation, self.__duration + other.__duration)
    
    def __add__(self, other : 'Animator') -> 'Animator':
        return self.concat(other)

    def setElapsedTime(self, time : float) -> None:
        self.__elapsedTime = time

    def setTimeScale(self, timeScale : float) -> None:
        self.__timeScale = timeScale

    def setRepeatMode(self, mode : int) -> None:
        self.__repeatMode = mode if 0 <= mode <= 3 else 0
    
    def setHook(self, hook : Callable[[any], None]) -> None:
        self.__hook = hook
    
    def addHook(self, hook : Callable[[any], None]) -> None:
        if self.__hook is None:
            self.__hook = hook
        else:
            oldHook = self.__hook
            def newHook(p):
                oldHook(p)
                hook(p)
            self.__hook = newHook

    def detachHook(self) -> None:
        self.__hook = None
    
    def setEndCallback(self, callback : Callable[[], None]) -> None:
        self.__endCallback = callback

    def isRunning(self) -> bool:
        return self.__isRunning
    
    def getElapsedTime(self) -> float:
        return self.__elapsedTime
    
    def getTimeScale(self):
        return self.__timeScale

    def getRepeatMode(self):
        return self.__repeatMode
    
    
    @classmethod
    def mix(cls, mixFunction, start : any, end : any, duration : float) -> 'Animator':
        def equation(t : float) -> any:
            crntMix = mixFunction(t / duration)
            return start * (1 - crntMix) + end * crntMix
        return cls(equation, duration)

    @classmethod
    def lerp(cls, start : any, end : any, duration : float) -> 'Animator':
        return cls.mix(lambda t : t, start, end, duration)
    
    @classmethod
    def smoothLerp(cls, start : any, end : any, duration : float) -> 'Animator':
        return cls.mix(lambda t : -2*t*t*(t-1.5), start, end, duration)
    
    @classmethod
    def easeIn(cls, start : any, end : any, duration : float) -> 'Animator':
        return cls.mix(lambda t : t*t, start, end, duration)
    
    @classmethod
    def easeOut(cls, start : any, end : any, duration : float) -> 'Animator':
        return cls.mix(lambda t : (2-t)*t, start, end, duration)
    
    @classmethod
    def oscillate(cls, start : any, end : any, duration : float) -> 'Animator':
        return cls.mix(lambda t : -0.5*(math.cos(2*math.pi*t)-1), start, end, duration)
    
    @classmethod
    def step(cls, values : list[any], duration : float) -> 'Animator':
        equation = lambda t : values[min(int(t / duration * len(values)), len(values)-1)]
        return cls(equation, duration)

    @classmethod
    def const(cls, value : any, duration : float) -> 'Animator':
        return cls(lambda _ : value, duration)
    

    @staticmethod
    def updateAll(dt : float) -> None:
        for a in Animator._instances:
            a.update(dt)