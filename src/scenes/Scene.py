from typing import Callable
from weakref import WeakSet
from components.Component import Component
import pygame
import gc

from utils.Animator import Animator
from utils.Timer import Timer

class Scene:
    """
    A scene is a container for all components (thus logic) that can happen at one time in the game. An actuial scene should 

    Eg. One can seperate the hole game into a MenuScene and GameScene which are completely seperate from eachother.
    """

    def __init__(self, clearColor : tuple[int] = (0, 0, 0)):
        """
        In the constructor all components that are used should be created.

        If there are any components that have to be created later on you have to use SceneManager.requestComponent. Note that this component will be ready for use in the next frame.

        Args:
            clearColor (tuple[int], optional): The clear color of the scene. This is the color with which the whole screen will be replaced before the drawign of a frame. Defaults to (0, 0, 0).
        """
        self.__clearColor = clearColor

    def start(self) -> None:
        """
        Will be called when the Scene has finished loading.
        """
        pass

    def getClearColor(self) -> tuple[int]:
        """
        Returns the clear color of the scene. This is the color with which the whole screen will be replaced before the drawign of a frame.

        Returns:
            tuple[int]: The clear color of the scene. This is the color with which the whole screen will be replaced before the drawign of a frame.
        """
        return self.__clearColor



class SceneManager:
    """
    This static class manages Scene creating, loading and destroying.

    It is also in charge of drawing and late component creation.
    """

    __currentScene : Scene = None
    __requestedScene : type[Scene] = None

    __componentCreators : list[Callable[[], Component]] = []

    __drawables : list[WeakSet[Component]] = [ WeakSet(), WeakSet(), WeakSet() ]

    MAIN_LAYER = 0
    OVERLAY_LAYER = 1
    SEC_OVERLAY_LAYER = 2


    @staticmethod
    def loadNewSceneIfRequested() -> None:
        """
        Loads a new scene and destroys the old one if a scene has been requested during the last frame.
        """
        if SceneManager.__requestedScene != None:
            SceneManager.__clearAllInstances()
            
            SceneManager.__currentScene = SceneManager.__requestedScene()
            SceneManager.__currentScene.start()

            SceneManager.__requestedScene = None

            # garbage collect all unnecessary instances in regestries
            gc.collect()
    
    @staticmethod
    def __clearAllInstances():
        """
        Clears all instances in all scene related registries (Component, Animator, Timer).
        """
        Component.clearInstances()
        Animator.clearInstances()
        Timer.clearInstances()

        SceneManager.__drawables = [ WeakSet(), WeakSet(), WeakSet() ]

    
    @staticmethod
    def requestloadScene(scene : type[Scene]) -> None:
        """
        Request a scene. (see loadNewSceneIfRequested)

        Args:
            scene (type[Scene]): The scene type that should be loaded.
        """
        SceneManager.__requestedScene = scene

    
    @staticmethod
    def putInDrawLayer(c : Component | list[Component], layer : int = MAIN_LAYER) -> None:
        """
        Registers a component or a list of components as drawables. In later frames its draw method will be called.

        The draw layer determines in which order all components should be drawn. The draw layers will be drawn in this order:
        1. MAIN_LAYER
        2. OVERLAY_LAYER
        3. SEC_OVERLAY_LAYER

        Within one draw layer the draw order is not standardized.

        Args:
            c (Component | list[Component]): The component or the list of components that should be registered as drawables. 
            layer (int, optional): The draw layer in which the component(s) should be drawn. Defaults to MAIN_LAYER.
        """
        if isinstance(c, list):
            for x in c:
                SceneManager.__drawables[layer].add(x)
        else:
            SceneManager.__drawables[layer].add(c)
    
    @staticmethod
    def drawAll(screen : pygame.Surface) -> None:
        """
        Draws all registered components on the specified order (see putInDrawLayer) to the screen.

        Args:
            screen (pygame.Surface): The screen surface which the components will be drawn to.
        """
        for layerSet in SceneManager.__drawables:
            for c in layerSet:
                c.draw(screen)
    
    @staticmethod
    def getClearColor() -> tuple[int]:
        """
        Returns the clear color of the current scene.

        Returns:
            tuple[int]: The clear color of the current scene.
        """
        return SceneManager.__currentScene.getClearColor()
    
    @staticmethod
    def requestComponent(componentCreator : Callable[[], Component]) -> None:
        """
        Requests a late component creation.

        The creation will take place at the end of the frame. Thus the component will be ready for use in the next frame.

        Args:
            componentCreator (Callable[[], Component]): This callback should execute the component creation (eg calling the constructor and place it in the correct memory space).
        """
        SceneManager.__componentCreators.append(componentCreator)

    @staticmethod
    def createRequestedComponents() -> None:
        """
        Executes all requested component creations.

        Should be called at the end of a frame.
        """
        for cr in SceneManager.__componentCreators:
            cr()
        
        SceneManager.__componentCreators = []