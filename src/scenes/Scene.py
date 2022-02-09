from typing import Callable
from weakref import WeakSet
from components.Component import Component
import pygame
import gc

class Scene:

    def __init__(self, clearColor : tuple[int] = (0, 0, 0)):
        self.__clearColor = clearColor

    def start(self) -> None:
        pass

    def destroy(self) -> None:
        pass

    def getClearColor(self) -> tuple[int]:
        return self.__clearColor



class SceneManager:

    __currentScene : Scene = None
    __requestedScene : type[Scene] = None

    __componentCreators : list[Callable[[], Component]] = []

    __drawables : list[WeakSet[Component]] = [ WeakSet(), WeakSet(), WeakSet() ]

    MAIN_LAYER = 0
    OVERLAY_LAYER = 1
    SEC_OVERLAY_LAYER = 2


    @staticmethod
    def loadNewSceneIfRequested() -> None:
        if SceneManager.__requestedScene != None:
            if SceneManager.__currentScene != None:
                SceneManager.__currentScene.destroy()
            
            
            SceneManager.__currentScene = SceneManager.__requestedScene()
            SceneManager.__currentScene.start()

            SceneManager.__requestedScene = None

            # garbage collect all unnecessary instances in regestries
            gc.collect()

    
    @staticmethod
    def requestloadScene(scene : type[Scene]) -> None:
        SceneManager.__requestedScene = scene

    
    @staticmethod
    def putInDrawLayer(c : Component | list[Component], layer : int = MAIN_LAYER) -> None:
        if isinstance(c, list):
            for x in c:
                SceneManager.__drawables[layer].add(x)
        else:
            SceneManager.__drawables[layer].add(c)
    
    @staticmethod
    def drawAll(screen : pygame.Surface) -> None:
        for layerSet in SceneManager.__drawables:
            for c in layerSet:
                c.draw(screen)
    
    @staticmethod
    def getClearColor() -> tuple[int]:
        return SceneManager.__currentScene.getClearColor()
    
    @staticmethod
    def requestComponent(componentCreator : Callable[[], Component]) -> None:
        SceneManager.__componentCreators.append(componentCreator)

    @staticmethod
    def createRequestedComponents() -> None:
        for cr in SceneManager.__componentCreators:
            cr()
        
        SceneManager.__componentCreators = []