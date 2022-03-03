from components.ui.ImageButton import ImageButton
from utils.Images import Sprite
from utils.Input import Input
from utils.Transform import Transform


class Checkbox(ImageButton):
    """
    Represents a checkbox.
    """

    def __init__(self, scaleFactor : float = 0.8, inputLayer : int = Input.GAME_LAYER, transform : Transform = None):
        """
        Constructor of the Checkbox class.

        Args:
            scaleFactor (float, optional): How much scales the button when teh checkbox is pressed. Defaults to 0.8.
            inputLayer (int, optional): The input layer of the AbstractButton. If that layer doesn't match the current input layer (see Input class), the button won't be clickable. Defaults to Input.GAME_LAYER.
            transform (Transform, optional): The Transform of the component. Defaults to None.
        """
        self.__substituteSprite = Sprite("buttons.checkbox_active")
        self.__isActive = False
        super().__init__("buttons.checkbox_idle", scaleFactor, inputLayer, transform)

        self.__substituteSprite.transform.setParent(self.transform)
        self.__substituteSprite.bakeTransform()
    
    def isActive(self) -> bool:
        """
        Returns whether the button is currently checked.

        Returns:
            bool: If the button is currently checked.
        """
        return self.__isActive

    def toggle(self) -> None:
        """
        Toggle the active state of the checkbox.

        It also updates the graphics.
        """
        self.__isActive = not self.__isActive
        self._sprite, self.__substituteSprite = self.__substituteSprite, self._sprite
    
    def setActive(self, value : bool) -> None:
        """
        Sets the active state. 

        It also updates the graphics.
        Args:
            value (bool): The active state
        """
        if value != self.__isActive:
            self.toggle()
    
    def onMouseUp(self) -> None:
        super().onMouseUp()
        self.toggle()
    
    def onPressCancel(self) -> None:
        super().onMouseUp()