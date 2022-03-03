import utils
import pygame


class Component(metaclass = utils.InstanceRegistryMetaClass):
    """
        Represents a plain component with a certain Transform.

        By deriving from it, it is possible to add behavior and graphics to it.
        To do that, just override the update and draw methods.
        
        The update method will be called automatically by the Registry. For the draw method to be called, it has to by registered in the SceneManager using putInDrawLayer.

        Within a scene's update or draw method you should not simply create a component as that will crash the game. Instead you have to use SceneManager.requestComponent(). 
        
        Attributes:
            transform (Transform): The position, rotation and scale of the Component. In some curcumstances this might be not necessary. In this case just use None as the Transform. This will create an identity TRansform for the Component.
    """

    def __init__(self, transform : utils.Transform):
        """
        Constructor of the Component class.

        Args:
            transform (Transform): The position, rotation and scale of the Component. In some curcumstances this might be not necessary. In this case just use None as the Transform. This will create an identity TRansform for the Component.
        """
        self.transform : utils.Transform = utils.Transform.fromTransform(transform)

    def update(self, dt : float) -> None:
        """
        Holds the behavior of the Component. It should be overwritten.

        It will be called automatically by the Registry

        Args:
            dt (float): Time that past since the last frame in seconds.
        """
        pass

    def draw(self, screen : pygame.Surface) -> None:
        """
        Hold any graphical behavior of the Component. It should be overwritten.
        
        For it to be called, it has to by registered in the SceneManager using putInDrawLayer

        Args:
            screen (pygame.Surface): The screen surface on which you should draw using pygame.
        """
        pass

    @staticmethod
    def updateAll(dt : float) -> None:
        """
        Calls the update method of all Components in the Registry. Should only be called by main.

        Args:
            dt (float): Time that past since the last frame in seconds.
        """
        for c in Component._instances:
            c.update(dt)