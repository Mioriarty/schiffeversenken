
from components.Component import Component
from components.ui.ImageButton import ImageButton
from scenes.Scene import SceneManager
from utils.Animator import Animator
from utils.Images import Sprite
import numpy as np

from utils.Transform import Transform


class DifficultySelect(Component):

    TEXT_SCALE = (0.5, 0.5)
    MOVE_DURATION = 0.2

    def __init__(self, transform : Transform = None):
        super().__init__(transform)

        self.options = [
            ( Sprite('texts.kaptnBlaubar', Transform(scale=DifficultySelect.TEXT_SCALE, parent=self.transform), bakeNow=True), 0.8 ),
            ( Sprite('texts.captainHook',  Transform(scale=DifficultySelect.TEXT_SCALE, parent=self.transform), bakeNow=True), 0.5 ),
            ( Sprite('texts.dieWilde13',   Transform(scale=DifficultySelect.TEXT_SCALE, parent=self.transform), bakeNow=True), 0.2 ),
            ( Sprite('texts.jackSparrow',  Transform(scale=DifficultySelect.TEXT_SCALE, parent=self.transform), bakeNow=True), 0.0 )
        ]

        self.selectedIndex = 0
        SceneManager.putInDrawLayer(self.options[0][0], SceneManager.UI_MAIN_LAYER)
        for i in range(1, len(self.options)):
            SceneManager.putInDrawLayer(self.options[i][0], SceneManager.UI_MAIN_LAYER)
            self.options[i][0].image.set_alpha(0)
        
        self.appearLeftMove = Animator.lerp(np.array((-200, 0)), np.zeros(2 ), DifficultySelect.MOVE_DURATION)
        self.appearRightMove = Animator.lerp(np.array((200, 0)), np.zeros(2), DifficultySelect.MOVE_DURATION)
        self.appearAlpha = Animator.lerp(0., 255., DifficultySelect.MOVE_DURATION)

        self.disappearLeftMove = Animator.lerp(np.zeros(2), np.array((-200, 0)), DifficultySelect.MOVE_DURATION)
        self.disappearRightMove = Animator.lerp(np.zeros(2), np.array((200, 0)), DifficultySelect.MOVE_DURATION)
        self.disappearAlpha = Animator.lerp(255., 0., DifficultySelect.MOVE_DURATION)
        
        self.leftButton = ImageButton(Sprite("buttons.left"), transform = Transform((-300, 0), scale=(0.2, 0.2), parent=self.transform))
        self.leftButton.setOnClickEvent(self.leftPress)

        self.rightButton = ImageButton(Sprite("buttons.right"), transform = Transform((300, 0), scale=(0.2, 0.2), parent=self.transform))
        self.rightButton.setOnClickEvent(self.rightPress)

    def leftPress(self):
        self.skipAnimations()

        self.disappearLeftMove.setHook(self.options[self.selectedIndex][0].transform.setRelPosition)
        self.disappearAlpha.setHook(self.options[self.selectedIndex][0].image.set_alpha)

        self.selectedIndex = (self.selectedIndex - 1 + len(self.options)) % len(self.options)

        self.appearRightMove.setHook(self.options[self.selectedIndex][0].transform.setRelPosition)
        self.appearAlpha.setHook(self.options[self.selectedIndex][0].image.set_alpha)

        self.disappearLeftMove.replay()
        self.disappearAlpha.replay()
        self.appearRightMove.replay()
        self.appearAlpha.replay()
        

    def rightPress(self):
        self.skipAnimations()

        self.disappearRightMove.setHook(self.options[self.selectedIndex][0].transform.setRelPosition)
        self.disappearAlpha.setHook(self.options[self.selectedIndex][0].image.set_alpha)

        self.selectedIndex = (self.selectedIndex + 1) % len(self.options)

        self.appearLeftMove.setHook(self.options[self.selectedIndex][0].transform.setRelPosition)
        self.appearAlpha.setHook(self.options[self.selectedIndex][0].image.set_alpha)

        self.disappearRightMove.replay()
        self.disappearAlpha.replay()
        self.appearLeftMove.replay()
        self.appearAlpha.replay()
    
    def skipAnimations(self):
        if self.disappearLeftMove.isRunning():
            self.disappearLeftMove.skipToEnd()
            self.appearRightMove.skipToEnd()

            self.disappearAlpha.skipToEnd()
            self.appearAlpha.skipToEnd()

        elif self.disappearRightMove.isRunning():
            self.disappearRightMove.skipToEnd()
            self.appearLeftMove.skipToEnd()

            self.disappearAlpha.skipToEnd()
            self.appearAlpha.skipToEnd()
        
        