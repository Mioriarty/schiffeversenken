from components.ambient.Fish import Fish
from scenes.Scene import Scene, SceneManager
from components.Rectangle import Rectangle
from utils import Animator, Transform, Sprite
import numpy as np

class TestScene(Scene):

    def __init__(self):
        self.fish = Fish([200, 200])
        SceneManager.putInDrawLayer(self.fish, SceneManager.GAME_MAIN_LAYER)

        self.r = Rectangle(Transform((100, 100), 20, (1, 0.5)), 100, 100)
        self.a = Animator.smoothLerp(0, 1.51, 5) + Animator.easeOut(1.51, 4, 2)
        self.a.setRepeatMode(Animator.REVERSE)
        self.a.setHook(self.r.transform.setRelAngle)

        self.a2 = Animator.oscillate(np.array([100, 50]), np.array([400, 800]), 10)
        self.a2.setRepeatMode(Animator.RESTART)
        self.a2.setHook(self.r.transform.setRelPosition)

        SceneManager.putInDrawLayer(self.r, SceneManager.GAME_BG_LAYER)

        self.paper = Sprite("bg.paper", Transform.screenCenter(scale=(1.1, 1.1)))
        SceneManager.putInDrawLayer(self.paper, SceneManager.BG_OVERLAY_LAYER)

        self.wood = Sprite("bg.wood", Transform.screenCenter())
        SceneManager.putInDrawLayer(self.wood, SceneManager.BG_MAIN_LAYER)

    
    def start(self) -> None:
        self.a.play()
        self.a2.play()