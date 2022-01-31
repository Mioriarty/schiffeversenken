from scenes.Scene import Scene, SceneManager
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Transform import Transform

class GameScene(Scene):

    START_ANIM_TIME = 3.5
    
    def __init__(self):
        super().__init__((255, 255, 255))

        self.landParent = Transform()
        self.land = Sprite("ambient.land", Transform.screenCenter(y = 75, scale=(0.5, 0.5), parent=self.landParent), bakeNow=True)
        SceneManager.putInDrawLayer(self.land, SceneManager.GAME_MAIN_LAYER)

        self.landAppearAnim = Animator.easeOut(-250, 0, GameScene.START_ANIM_TIME)
        self.landAppearAnim.setHook(self.landParent.setRelYPos)
        self.landAppearAnim.play()

        self.board1 = Sprite("game.board", Transform((230, 480), scale=(0.35, 0.35)), bakeNow=True)
        self.board2 = Sprite("game.board", Transform((790, 480), scale=(0.35, 0.35)), bakeNow=True)
        SceneManager.putInDrawLayer([ self.board1, self.board2], SceneManager.GAME_BG_LAYER)

        self.boardAppearAnim = Animator.smoothLerp(0., 150., GameScene.START_ANIM_TIME)
        self.boardAppearAnim.setHook(self.board1.image.set_alpha)
        self.boardAppearAnim.addHook(self.board2.image.set_alpha)

        self.boardAppearAnim.play()

        