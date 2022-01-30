
from ai.Difficulties import Difficulties
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

        self.selectedIndex = 0

        self.nameImages = [ Sprite(img, Transform(scale=DifficultySelect.TEXT_SCALE, parent=self.transform), bakeNow=True) for img in Difficulties.allNameImages() ]
        for i in range(1, len(self.nameImages)):
            self.nameImages[i].image.set_alpha(0)
        SceneManager.putInDrawLayer(self.nameImages, SceneManager.UI_MAIN_LAYER)
        
        self.appearLeftMove = Animator.easeOut(np.array((-250, 0)), np.zeros(2 ), DifficultySelect.MOVE_DURATION)
        self.appearRightMove = Animator.easeOut(np.array((250, 0)), np.zeros(2), DifficultySelect.MOVE_DURATION)
        self.appearAlpha = Animator.lerp(0., 255., DifficultySelect.MOVE_DURATION)

        self.disappearLeftMove = Animator.easeIn(np.zeros(2), np.array((-250, 0)), DifficultySelect.MOVE_DURATION)
        self.disappearRightMove = Animator.easeIn(np.zeros(2), np.array((250, 0)), DifficultySelect.MOVE_DURATION)
        self.disappearAlpha = Animator.lerp(255., 0., DifficultySelect.MOVE_DURATION)
        
        self.leftButton = ImageButton(Sprite("buttons.left"), transform = Transform((-300, 0), scale=(0.2, 0.2), parent=self.transform))
        self.leftButton.setOnClickEvent(self.leftPress)

        self.rightButton = ImageButton(Sprite("buttons.right"), transform = Transform((300, 0), scale=(0.2, 0.2), parent=self.transform))
        self.rightButton.setOnClickEvent(self.rightPress)

    def rightPress(self):
        self.skipAnimations()

        self.disappearLeftMove.setHook(self.nameImages[self.selectedIndex].transform.setRelPosition)
        self.disappearAlpha.setHook(self.nameImages[self.selectedIndex].image.set_alpha)

        self.selectedIndex = (self.selectedIndex + 1) % len(self.nameImages)

        self.appearRightMove.setHook(self.nameImages[self.selectedIndex].transform.setRelPosition)
        self.appearAlpha.setHook(self.nameImages[self.selectedIndex].image.set_alpha)

        self.disappearLeftMove.replay()
        self.disappearAlpha.replay()
        self.appearRightMove.replay()
        self.appearAlpha.replay()

        Difficulties.setSelectedIndex(self.selectedIndex)
        

    def leftPress(self):
        self.skipAnimations()

        self.disappearRightMove.setHook(self.nameImages[self.selectedIndex].transform.setRelPosition)
        self.disappearAlpha.setHook(self.nameImages[self.selectedIndex].image.set_alpha)

        self.selectedIndex = (self.selectedIndex - 1 + len(self.nameImages)) % len(self.nameImages)

        self.appearLeftMove.setHook(self.nameImages[self.selectedIndex].transform.setRelPosition)
        self.appearAlpha.setHook(self.nameImages[self.selectedIndex].image.set_alpha)

        self.disappearRightMove.replay()
        self.disappearAlpha.replay()
        self.appearLeftMove.replay()
        self.appearAlpha.replay()

        Difficulties.setSelectedIndex(self.selectedIndex)
    
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
        
        