import pygame
from components.ambient.Bird import Bird
from components.ambient.Diashow import Diashow
from components.ambient.RandomAmbientEvent import Shark
from components.ui.ImageButton import ImageButton
import scenes.game.GameScene
from scenes.Scene import Scene, SceneManager
from scenes.menu.DifficultySelect import DifficultySelect
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Sounds import Sounds
from utils.Transform import Transform
import numpy as np


class MenuScene(Scene):

    def __init__(self):
        super().__init__((255, 255, 255))
        Sounds.playMusic("aquaWaves")

        self.parentTransform = Transform()
        self.gameStartAnimation = Animator.easeIn(np.zeros(2), np.array((0, -800)), .8)
        self.gameStartAnimation.setHook(self.parentTransform.setRelPosition)
        self.gameStartAnimation.setEndCallback(self.startGame)

        self.headingSprite = Sprite("texts.seeschlacht", Transform.screenCenter(y = 100., scale=(0.5, 0.5), parent=self.parentTransform), bakeNow=True)
        SceneManager.putInDrawLayer(self.headingSprite)

        # self.gengnerSprite = Sprite("texts.gegner", Transform.screenCenter(y=230., scale=(0.3, 0.3), parent=self.parentTransform), bakeNow=True)
        # SceneManager.putInDrawLayer(self.gengnerSprite, SceneManager.UI_MAIN_LAYER)
    
        self.difficultySelect = DifficultySelect(Transform.screenCenter(y = 280., parent=self.parentTransform))

        self.islands = [
            Diashow([ "ambient.island1", "ambient.island2" ], 0.5, transform=Transform((100, 200), scale=(0.4, 0.4), parent=self.parentTransform)),
            Diashow([ "ambient.island2", "ambient.island1" ], 0.5, transform=Transform((800, 650), scale=(0.4, 0.4), parent=self.parentTransform)) 
        ]
        SceneManager.putInDrawLayer(self.islands)

        self.playBtn = ImageButton(Sprite("buttons.spielen"), transform = Transform.screenCenter(y=600., scale=(0.3, 0.3), parent=self.parentTransform))
        self.playBtn.setOnClickEvent(self.gameStartAnimation.play)
        SceneManager.putInDrawLayer(self.playBtn)


        self.birds = [
            Bird(velocity = 60., transform=Transform(scale=(0.25, 0.25), parent=self.parentTransform)),
            Bird(velocity = 45., transform=Transform(scale=(0.36, 0.36), parent=self.parentTransform))
        ]
        SceneManager.putInDrawLayer(self.birds)

        self.shark = Shark(0.3, pygame.Rect(50, 350, 100, 300), (7., 15.), transform=Transform(scale=(0.3, 0.3), parent=self.parentTransform))
        SceneManager.putInDrawLayer(self.shark)

    
    def startGame(self):
        SceneManager.requestloadScene(scenes.game.GameScene.GameScene)
    