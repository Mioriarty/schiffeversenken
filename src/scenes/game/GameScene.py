from scenes.Scene import Scene, SceneManager
from scenes.game.Ship import Ship, ShipManager
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Transform import Transform
import math

class GameScene(Scene):

    START_ANIM_TIME = 0.01 # TODO: 3.5
    
    def __init__(self):
        super().__init__((255, 255, 255))

        self.landParent = Transform()
        self.land = Sprite("ambient.land", Transform.screenCenter(y = 75, scale=(0.5, 0.5), parent=self.landParent), bakeNow=True)
        SceneManager.putInDrawLayer(self.land, SceneManager.GAME_MAIN_LAYER)

        self.landAppearAnim = Animator.easeOut(-250, 0, GameScene.START_ANIM_TIME)
        self.landAppearAnim.setHook(self.landParent.setRelYPos)
        self.landAppearAnim.play()

        self.board1 = Sprite("game.board", Transform((250, 480), scale=(0.4, 0.4)), bakeNow=True)
        self.board2 = Sprite("game.board", Transform((770, 480), scale=(0.4, 0.4)), bakeNow=True)
        SceneManager.putInDrawLayer([ self.board1, self.board2], SceneManager.GAME_BG_LAYER)

        self.boardAppearAnim = Animator.smoothLerp(0., 150., GameScene.START_ANIM_TIME)
        self.boardAppearAnim.setHook(self.board1.image.set_alpha)
        self.boardAppearAnim.addHook(self.board2.image.set_alpha)
        self.boardAppearAnim.play()

        self.shipManager = ShipManager([
            Ship(2, transform=Transform((310, 140), angle=-math.pi/2,  parent=self.landParent)),
            Ship(2, transform=Transform((375, 95), angle=-math.pi/2,  parent=self.landParent)),
            Ship(2, transform=Transform((110, 80), angle=-2.5,  parent=self.landParent)),
            Ship(2, transform=Transform((70, 110), angle=-2.3,  parent=self.landParent)),

            Ship(3, transform=Transform((226, 160), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, transform=Transform((254, 158), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, transform=Transform((281, 155), angle=-math.pi/2,  parent=self.landParent)),

            Ship(4, transform=Transform((200, 180), angle=-math.pi/2, parent=self.landParent)),
            Ship(4, transform=Transform((340, 120), angle=-math.pi/2, parent=self.landParent)),

            Ship(5, transform=Transform((170, 120), angle=-math.pi/2, parent=self.landParent))
        ], self.board1.image.get_rect(center=self.board1.transform.getPosition()), 11)
        
        SceneManager.putInDrawLayer(self.shipManager, SceneManager.GAME_MAIN_LAYER)

        