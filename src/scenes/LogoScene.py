from scenes.Scene import Scene, SceneManager
from utils import *

class LogoScene(Scene):

    def __init__(self) -> None:
        self.logo = Sprite("logos.mo", Transform.screenCenter())
        self.logo.transform.translate((0., -50.0))
        SceneManager.putInDrawLayer(self.logo, SceneManager.GAME_MAIN_LAYER)

        self.logoAnimation = Animator.smoothLerp(0.6, 1., 5)
        self.logoAnimation.setRepeatMode(Animator.PAUSE)
        self.logoAnimation.setHook(lambda s : self.logo.transform.setRelScale((s, s)))

        self.alphaAnimation = Animator.easeOut(0, 255., 1) + Animator.const(255, 4.3) + Animator.easeIn(255, 0, 1)
        self.alphaAnimation.setHook(self.logo.image.set_alpha)
    
    def start(self) -> None:
        Sounds.playSoundEffect("intro")
        self.logoAnimation.play()
        self.alphaAnimation.play()