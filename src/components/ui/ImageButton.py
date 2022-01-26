from components.ui.AbstractButton import AbstractButton
from scenes.Scene import SceneManager
from utils.Images import Sprite
from utils.Transform import Transform

class ImageButton(AbstractButton):

    def __init__(self, sprite : Sprite, scaleFactor : float = 0.8, transform : Transform = None):
        super().__init__(sprite.image.get_width(), sprite.image.get_height(), transform)
        self.__sprite = sprite
        self.__sprite.transform.setParent(self.transform)
        self.__sprite.bakeTransform()
        self.__scaleFactor = scaleFactor

        SceneManager.putInDrawLayer(self.__sprite, SceneManager.UI_MAIN_LAYER)
    
    def onMouseDown(self) -> None:
        self.__sprite.transform.scale(self.__scaleFactor)
        self.__sprite.bakeTransform()
    
    def onMouseUp(self) -> None:
        self.__sprite.transform.scale(1 / self.__scaleFactor)
        self.__sprite.bakeTransform()
    
    def onPressCancel(self) -> None:
        self.onMouseUp()