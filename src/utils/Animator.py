from utils.InstanceRegistryMetaClass import InstanceRegistryMetaClass
from typing import Callable
import math

class Animator(metaclass = InstanceRegistryMetaClass):
    """
    Represents an arbitrary animation of any kind of value. 

    An Animator basically holds a function and a current time. You can easily update the time and compute the current value of the function.

    Additionally you can bind the value of the animation directly to a certain value of eg a transform. Because in the game all animations are updated automatically (using the registry) this makes it really easy to eg smoothly move an component over the screen. 
    """

    STOP    = 0
    PAUSE   = 1
    RESTART = 2
    REVERSE = 3

    def __init__(self, equation : Callable[[float], any], duration : float):
        """
        The construcor of the Animator class.

        Args:
            equation (Callable[[float], any]): The function that can be evalated in the interval [0, duration].
            duration (float): The duration of the animation in seconds.
        """
        self.__equation : Callable[[float], any] = equation
        self.__duration : float                  = duration
        self.__elapsedTime : float               = 0
        self.__timeScale : float                 = 1
        self.__isRunning : bool                  = False
        self.__repeatMode : int                  = Animator.PAUSE
        self.__hook : Callable[[any], None]      = None
        self.__endCallback : Callable[[], None ] = None

    def play(self) -> None:
        """
        Starts or, if paused, resumes the animation.
        """
        self.__isRunning = True
    
    def replay(self) -> None:
        """
        Resets the time to 0 and plays the animation.
        """
        self.stop()
        self.play()

    def update(self, dt : float) -> None:
        """
        Updates the internal current time by dt. It will also fire any hooked methods and manges what happens when the end of the animation has reached.

        Args:
            dt (float): Th time that has passed since the last update in seconds.
        """
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
        """
        Returns the current value of the equation.

        Returns:
            any: The current value of the equation.
        """
        return self.__equation(self.__elapsedTime)
    
    def pause(self) -> None:
        """
        Pauses the animation.

        By calling play() it can be resumed.
        """
        self.__isRunning = False
    
    def stop(self) -> None:
        """
        Pauses the animation and resets all values to the origanal state.
        """
        self.__isRunning = False
        self.__elapsedTime = 0
        self.__timeScale = abs(self.__timeScale)
    
    def skipToEnd(self) -> None:
        """
        Jumps to the end of the animation and updates hooked values.

        If a repeat mode is set this will also be handeled accordingly.
        """
        self.__elapsedTime = self.__duration
        self.update(0)
    
    def concat(self, other : 'Animator') -> 'Animator':
        """
        Concatinates two animations.

        That means that the second animation will be played after the first animations.

        Any pre-bound hooks will be lost in the process.

        Args:
            other (Animator): This animation will be played secondly.

        Returns:
            Animator: The combined animation.
        """
        equation = lambda t : self.__equation(t) if t < self.__duration else other.__equation(t - self.__duration)
        return Animator(equation, self.__duration + other.__duration)
    
    def __add__(self, other : 'Animator') -> 'Animator':
        """
        Shortcut for concatination (see concat).

        Args:
            other (Animator): This animation will be played secondly.

        Returns:
            Animator: The combined animation.
        """
        return self.concat(other)
    
    def setEquation(self, equation : Callable[[float], any]) -> None:
        """
        Sets the equation.

        Args:
            equation (Callable[[float], any]): The function that can be evalated in the interval [0, duration].
        """
        self.__equation = equation

    def setElapsedTime(self, time : float) -> None:
        """
        Sets the current time.

        Args:
            time (float): The current time.
        """
        self.__elapsedTime = time

    def setTimeScale(self, timeScale : float) -> None:
        """
        Sets the time scale.

        If the time scale is negative, the animation will be played backwards. 

        Args:
            timeScale (float): The new time scale.
        """
        self.__timeScale = timeScale

    def setRepeatMode(self, mode : int) -> None:
        """
        Sets the repeat mode.

        This determines what happenes when the animation reaches its end. It can be:
        - STOP: Resets all values and than stops.
        - PAUSE: Doesn't reset any values and just stop.
        - RESTART: Resets all values and plays the animation again.
        - REVERSE: Doesn't reset any values and plays the animation backwards.

        Args:
            mode (int): The new repeat mode.
        """
        self.__repeatMode = mode if 0 <= mode <= 3 else 0
    
    def setHook(self, hook : Callable[[any], None]) -> None:
        """
        This binds an external value to the animation's current value.

        Args:
            hook (Callable[[any], None]): Callback that will be called each time the animation updates. This should set the external value accordingly. The parameter is that current animation value.
        """
        self.__hook = hook
    
    def addHook(self, hook : Callable[[any], None]) -> None:
        """
        Adds another hook to the animation (see setHook for details).

        Args:
            hook (Callable[[any], None]): The additional callback.
        """
        if self.__hook is None:
            self.__hook = hook
        else:
            oldHook = self.__hook
            def newHook(p):
                oldHook(p)
                hook(p)
            self.__hook = newHook

    def detachHook(self) -> None:
        """
        Detaches all hooks from the animation.

        No external values will be updated anymore.
        """
        self.__hook = None
    
    def setEndCallback(self, callback : Callable[[], None]) -> None:
        """
        Sets the callbeck that will called when the animation has ended. 

        It will also be called when the repeat mode is REPEAT or REVERSE

        Args:
            callback (Callable[[], None]): Callbeck that will called when the animation has ended. 
        """
        self.__endCallback = callback

    def isRunning(self) -> bool:
        """
        Checks whether the animation is not paused or stopped.

        Returns:
            bool: If the animation is not paused or stopped.
        """
        return self.__isRunning
    
    def getElapsedTime(self) -> float:
        """
        Returns the current internal time.

        Returns:
            float: The current internal time.
        """
        return self.__elapsedTime
    
    def getTimeScale(self) -> float:
        """
        Returns the time scale.

        Returns:
            float: The time scale.
        """
        return self.__timeScale

    def getRepeatMode(self) -> int:
        """
        Returns the repeat mode. See setRepeatMode for details.

        Returns:
            int: The repeat mode.
        """
        return self.__repeatMode
    
    def getDuration(self) -> float:
        """
        Returns the duration of the animation.

        Returns:
            float: The duration of the animation.
        """
        return self.__duration
    
    
    @classmethod
    def mix(cls, mixFunction, start : any, end : any, duration : float) -> 'Animator':
        """
        Creates an animation that mixes 2 values (start and end) based on a mix function.

        If T is the type of A and U is the type of B:
        - T should support: __mul__(float) and __add__(U)
        - U should support: __mul__(float) 

        The input of the mix function will be in [0, 1]. Thus it represents the ratio between the passed time and the total duration.

        Args:
            mixFunction (_type_): Function that mixes start and end together. The input will be in [0, 1]. Thus it represents the ratio between the passed time and the total duration.
            start (any): First value that mill be mixed.
            end (any): Second value that will be mixed.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        def equation(t : float) -> any:
            crntMix = mixFunction(t / duration)
            return start * (1 - crntMix) + end * crntMix
        return cls(equation, duration)

    @classmethod
    def lerp(cls, start : any, end : any, duration : float) -> 'Animator':
        """
        Creates a basic linear interpolation animation between start and end.

        For requirements of the types of start and end see Animator.mix.

        Args:
            start (any): The starting value of the animtion.
            end (any): The final value of the animation.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        return cls.mix(lambda t : t, start, end, duration)
    
    @classmethod
    def smoothLerp(cls, start : any, end : any, duration : float) -> 'Animator':
        """
        Creates a smooth interpolation animation between start and end.

        For requirements of the types of start and end see Animator.mix.

        Args:
            start (any): The starting value of the animtion.
            end (any): The final value of the animation.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        return cls.mix(lambda t : -2*t*t*(t-1.5), start, end, duration)
    
    @classmethod
    def easeIn(cls, start : any, end : any, duration : float) -> 'Animator':
        """
        Creates a interpolation animation between start and end where the animation is smoothed out at its start.

        For requirements of the types of start and end see Animator.mix.

        Args:
            start (any): The starting value of the animtion.
            end (any): The final value of the animation.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        return cls.mix(lambda t : t*t, start, end, duration)
    
    @classmethod
    def easeOut(cls, start : any, end : any, duration : float) -> 'Animator':
        """
        Creates a interpolation animation between start and end where the animation is smoothed out at its end.

        For requirements of the types of start and end see Animator.mix.

        Args:
            start (any): The starting value of the animtion.
            end (any): The final value of the animation.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        return cls.mix(lambda t : (2-t)*t, start, end, duration)
    
    @classmethod
    def oscillate(cls, start : any, end : any, duration : float) -> 'Animator':
        """
        Creates one oscillation between the start and end.

        For requirements of the types of start and end see Animator.mix.

        Args:
            start (any): The starting and final value of the animtion.
            end (any): The intermediate value of the animation.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        return cls.mix(lambda t : -0.5*(math.cos(2*math.pi*t)-1), start, end, duration)
    
    @classmethod
    def step(cls, values : list[any], duration : float) -> 'Animator':
        """
        Creates an animator that steps between the given values in even time intervals.

        The types of the values do not have any requirements. 

        Args:
            values (list[any]): The values that the animation will interate through.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        equation = lambda t : values[min(int(t / duration * len(values)), len(values)-1)]
        return cls(equation, duration)

    @classmethod
    def const(cls, value : any, duration : float) -> 'Animator':
        """
        Returns an animator that only holds one contant value at any time.

        Can be used eg. for movement pauses.

        Args:
            value (any): The constant value.
            duration (float): The duration of the resulting animation.

        Returns:
            Animator: The created animator.
        """
        return cls(lambda _ : value, duration)
    

    @staticmethod
    def updateAll(dt : float) -> None:
        """
        updates all Animators in the registry.

        Args:
            dt (float): Time that past during the last frame.
        """
        for a in Animator._instances:
            a.update(dt)