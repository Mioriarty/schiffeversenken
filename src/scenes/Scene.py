from weakref import WeakSet
from components.Component import Component
import pygame
import gc

class Scene:

    def start(self) -> None:
        pass

    def destroy(self) -> None:
        pass



class SceneManager:

    __currentScene : Scene = None
    __requestedScene : type[Scene] = None

    __drawables : list[WeakSet] = [ WeakSet(), WeakSet(), WeakSet(), WeakSet(), WeakSet(), WeakSet(), WeakSet() ]

    UI_BG_LAYER = 5
    UI_MAIN_LAYER = 6

    GAME_BG_LAYER = 2
    GAME_MAIN_LAYER = 3
    GAME_OVERLAY_LAYER = 4

    BG_MAIN_LAYER = 0
    BG_OVERLAY_LAYER = 1

    @staticmethod
    def tryLoadRequestedScene() -> None:
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
    def putInDrawLayer(c : Component | list[Component], layer : int) -> None:
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

