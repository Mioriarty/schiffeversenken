import pygame
from components.Component import Component
from components.ui.AbstractButton import AbstractButton
from components.ui.Checkbox import Checkbox
from components.ui.ImageButton import ImageButton
from utils.Images import Sprite
from utils.Transform import Transform


class SettingsSign(Component):

    def __init__(self):
        super().__init__(Transform.screenCenter())
        self.__show = False

        self.sign = Sprite("signs.settings", Transform(parent=self.transform))
        self.musicToggle = Checkbox(inputLayer=AbstractButton.SETTINGS_LAYER, transform=Transform((-235, -17), scale=(.7, .7), parent=self.transform))
        self.soundToggle = Checkbox(inputLayer=AbstractButton.SETTINGS_LAYER, transform=Transform((30, -20), scale=(.7, .7), parent=self.transform))

        self.backBtn = ImageButton("buttons.back", inputLayer=AbstractButton.SETTINGS_LAYER, transform=Transform((-10, 100), scale=(0.6, 0.6), parent=self.transform))
        self.backBtn.setOnClickEvent(self.hide)

    def draw(self, screen: pygame.Surface) -> None:
        if self.__show:
            self.sign.draw(screen)
            self.musicToggle.draw(screen)
            self.soundToggle.draw(screen)
            self.backBtn.draw(screen)
    
    def show(self) -> None:
        self.__show = True
        AbstractButton.setInputLayer(AbstractButton.SETTINGS_LAYER)

    
    def hide(self) -> None:
        self.__show = False
        AbstractButton.setInputLayer(AbstractButton.GAME_LAYER)