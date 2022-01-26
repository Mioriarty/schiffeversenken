from scenes.MenuScene import MenuScene
from scenes.Scene import Scene, SceneManager
from scenes.TestScene import TestScene
from utils import *

class LogoScene(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.logo = Sprite("logos.mo", Transform.screenCenter())
        self.logo.transform.translate((0., -50.0))
        self.logo.enableScaling = True
        SceneManager.putInDrawLayer(self.logo, SceneManager.GAME_MAIN_LAYER)

        self.logoAnimation = Animator.smoothLerp(0.6, 1., 5)
        self.logoAnimation.setRepeatMode(Animator.PAUSE)
        self.logoAnimation.setHook(lambda s : self.logo.transform.setRelScale((s, s)))

        self.alphaAnimation = Animator.easeOut(0, 255., 1) + Animator.const(255, 4.3) + Animator.easeIn(255, 0, 1)
        self.alphaAnimation.setHook(self.logo.image.set_alpha)
        self.alphaAnimation.setEndCallback(lambda : SceneManager.requestloadScene(MenuScene))
    
    def start(self) -> None:
        Sounds.playSoundEffect("intro")
        self.logoAnimation.play()
        self.alphaAnimation.play()