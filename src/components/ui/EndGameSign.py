
from components.Component import Component
from components.ui.AbstractButton import AbstractButton
from components.ui.ImageButton import ImageButton
from scenes.Scene import SceneManager
import scenes.menu.MenuScene
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Transform import Transform
import pygame


class EndGameSign(Component):

    ANIM_OFFSET = 30

    def __init__(self, transform: Transform = None):
        super().__init__(transform)

        self.winSign = ImageButton("signs.win", scaleFactor=1., inputLayer=AbstractButton.UI_LAYER, transform=self.transform)
        self.loseSign = ImageButton("signs.lose", scaleFactor=1., inputLayer=AbstractButton.UI_LAYER, transform=self.transform)
        self.__showWin = False
        self.__show = False

        self.winSign.setOnClickEvent(EndGameSign.__press)
        self.loseSign.setOnClickEvent(EndGameSign.__press)

        goalY = self.transform.getRelPosition()[1]
        self.anim = Animator.easeOut(-200., goalY + EndGameSign.ANIM_OFFSET, .5) + Animator.smoothLerp(goalY + EndGameSign.ANIM_OFFSET, goalY, .2)
     

    def draw(self, screen: pygame.Surface) -> None:
        if self.__show:
            if self.__showWin:
                self.winSign.draw(screen)
            else:
                self.loseSign.draw(screen)

    def __press():
        AbstractButton.setInputLayer(AbstractButton.GAME_LAYER)
        SceneManager.requestloadScene(scenes.menu.MenuScene.MenuScene)
    
    def show(self, won : bool):
        self.__show = True
        self.__showWin = won
        AbstractButton.setInputLayer(AbstractButton.UI_LAYER)

        if won:
            self.anim.setHook(self.winSign.transform.setRelYPos)
            self.winSign.enable()
        else:
            self.anim.setHook(self.loseSign.transform.setRelYPos)
            self.loseSign.enable()
        
        self.anim.play()
