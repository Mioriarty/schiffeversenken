import pygame
from components.Component import Component
from components.ui.AbstractButton import AbstractButton
from components.ui.Checkbox import Checkbox
from components.ui.ImageButton import ImageButton
from utils.Images import Sprite
from utils.Sounds import Sounds
from utils.Transform import Transform


class SettingsSign(Component):

    def __init__(self):
        super().__init__(Transform.screenCenter(scale=(0.9, 0.9)))
        self.__show = False

        self.transform.translate((0, -50))

        self.sign = Sprite("signs.settings", Transform(parent=self.transform), bakeNow=True)
        self.musicToggle = Checkbox(inputLayer=AbstractButton.SETTINGS_LAYER, transform=Transform((-235, -17), scale=(.7, .7), parent=self.transform))
        self.musicToggle.setActive(Sounds.isMusicOn())
        self.musicToggle.setOnClickEvent(lambda : Sounds.setMusicOn(self.musicToggle.isActive()))
        
        self.soundToggle = Checkbox(inputLayer=AbstractButton.SETTINGS_LAYER, transform=Transform((30, -20), scale=(.7, .7), parent=self.transform))
        self.soundToggle.setActive(Sounds.areSoundsOn())
        self.soundToggle.setOnClickEvent(lambda : Sounds.setSoundsOn(self.soundToggle.isActive()))


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