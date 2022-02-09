from components.ui.EndGameSign import EndGameSign
from components.ui.ImageButton import ImageButton
from scenes.Scene import Scene, SceneManager
from scenes.game.ShipPlacer import Ship, ShipPlacer
from scenes.game.TargetSelector import TargetSelector
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Sounds import Sounds
from utils.Transform import Transform
import math

class GameScene(Scene):

    START_ANIM_TIME = 0.01 # TODO: 3.5
    
    def __init__(self):
        super().__init__((255, 255, 255))

        self.landParent = Transform()
        self.land = Sprite("ambient.land", Transform.screenCenter(y = 75, scale=(0.5, 0.5), parent=self.landParent), bakeNow=True)
        SceneManager.putInDrawLayer(self.land)

        self.landAppearAnim = Animator.easeOut(-250, 0, GameScene.START_ANIM_TIME)
        self.landAppearAnim.setHook(self.landParent.setRelYPos)
        self.landAppearAnim.play()

        self.board1 = Sprite("game.board", Transform((250, 480), scale=(0.4, 0.4)), bakeNow=True)
        self.board2 = Sprite("game.board", Transform((770, 480), scale=(0.4, 0.4)), bakeNow=True)
        SceneManager.putInDrawLayer([ self.board1, self.board2])

        self.boardAppearAnim = Animator.smoothLerp(0., 150., GameScene.START_ANIM_TIME)
        self.boardAppearAnim.setHook(self.board1.image.set_alpha)
        self.boardAppearAnim.addHook(self.board2.image.set_alpha)
        self.boardAppearAnim.play()

        placementDoneBtn = ImageButton(Sprite("buttons.spielen"), transform = Transform.screenCenter(y=200., scale=(0.2, 0.2)))
        placementDoneBtn.setOnClickEvent(self.__placementDoneCallback)

        self.shipManager = ShipPlacer([
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
        ], placementDoneBtn, self.board1.image.get_rect(center=self.board1.transform.getPosition()), 11)
        
        SceneManager.putInDrawLayer(self.shipManager)

        self.oppositeShips = [
            Ship(2, onlyVisual=True, transform=Transform((800, 140), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, onlyVisual=True, transform=Transform((830, 160), angle=-math.pi/2,  parent=self.landParent))
        ]
        SceneManager.putInDrawLayer(self.oppositeShips)

        Ship.shipTotal = 10
        Ship.travelDoneCallback = self.__startGame

        self.targetSelector = TargetSelector(
            11,
            self.board1.image.get_rect(center=self.board1.transform.getPosition()),
            self.board2.image.get_rect(center=self.board2.transform.getPosition()),
            (100, 100),
            (600, 100),
            self.__gameEnded
        )
        SceneManager.putInDrawLayer(self.targetSelector)

        self.endGameSign = EndGameSign(transform=Transform.screenCenter())
        SceneManager.putInDrawLayer(self.endGameSign, SceneManager.OVERLAY_LAYER)

        self.endGameSign.show(False)


    
    def __placementDoneCallback(self):
        Sounds.playSoundEffect("ship_horn")
        for ship in self.oppositeShips:
            ship.doFakeTravel(self.board1.image.get_rect(center=self.board1.transform.getPosition()))
    

    def __startGame(self):
        self.targetSelector.setOwnShipPlacement(self.shipManager.getCurrentShipPlacement())
        self.targetSelector.start()
    
    def __gameEnded(self, won : bool) -> None:
        self.endGameSign.show(won)