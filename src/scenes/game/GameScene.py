import pygame
from components.ambient.Bird import Bird
from components.ambient.Diashow import Diashow
from components.ambient.RandomAmbientEvent import Shark
from components.game.Cannon import Cannon
from components.ui.AbstractButton import AbstractButton
from components.ui.EndGameSign import EndGameSign
from components.ui.ImageButton import ImageButton
from components.ui.SettingsSign import SettingsSign
from scenes.Scene import Scene, SceneManager
from scenes.game.ShipPlacer import Ship, ShipPlacer
from scenes.game.TargetSelector import TargetSelector
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Sounds import Sounds
from utils.Transform import Transform
import math

class GameScene(Scene):

    START_ANIM_TIME = 4. # TODO: 3.5
    
    def __init__(self):
        super().__init__((255, 255, 255))
        Ship.arrivedShips = 0
        AbstractButton.setInputLayer(AbstractButton.GAME_LAYER)

        self.landParent = Transform()
        self.land = Sprite("ambient.land3", Transform.screenCenter(y = 87.5, scale=(0.5, 0.5), parent=self.landParent), bakeNow=True)
        SceneManager.putInDrawLayer(self.land)

        self.landAppearAnim = Animator.easeOut(-280, 0, GameScene.START_ANIM_TIME)
        self.landAppearAnim.setHook(self.landParent.setRelYPos)
        self.landAppearAnim.play()

        self.board1 = Sprite("game.board", Transform((250, 520), scale=(0.4, 0.4)), bakeNow=True)
        self.board2 = Sprite("game.board", Transform((770, 520), scale=(0.4, 0.4)), bakeNow=True)
        SceneManager.putInDrawLayer([ self.board1, self.board2])

        self.boardAppearAnim = Animator.smoothLerp(0., 150., GameScene.START_ANIM_TIME)
        self.boardAppearAnim.setHook(self.board1.image.set_alpha)
        self.boardAppearAnim.addHook(self.board2.image.set_alpha)
        self.boardAppearAnim.play()

        placementDoneBtn = ImageButton("buttons.spielen", transform = Transform.screenCenter(y=200., scale=(0.2, 0.2)))
        placementDoneBtn.setOnClickEvent(self.__placementDoneCallback)

        self.shipManager = ShipPlacer([
            Ship(2, transform=Transform((302, 95), angle=-math.pi/2,  parent=self.landParent)),
            Ship(2, transform=Transform((350, 60), angle=-0.5,  parent=self.landParent)),
            Ship(2, transform=Transform((420, 100), angle=-0.5,  parent=self.landParent)),
            Ship(2, transform=Transform((45, 120), angle=-2.3,  parent=self.landParent)),

            Ship(3, transform=Transform((150, 170), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, transform=Transform((210, 163), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, transform=Transform((240, 160), angle=-math.pi/2,  parent=self.landParent)),

            Ship(4, transform=Transform((180, 187), angle=-math.pi/2, parent=self.landParent)),
            Ship(4, transform=Transform((270, 180), angle=-math.pi/2, parent=self.landParent)),

            Ship(5, transform=Transform((115, 150), angle=-math.pi/2, parent=self.landParent))
        ], placementDoneBtn, self.board1.image.get_rect(center=self.board1.transform.getPosition()), 11)
        
        SceneManager.putInDrawLayer(self.shipManager)

        self.oppositeShips = [
            Ship(2, onlyVisual=True, transform=Transform((795, 105), angle=-math.pi/2,  parent=self.landParent)),
            Ship(2, onlyVisual=True, transform=Transform((850, 100), angle=-math.pi/2,  parent=self.landParent)),
            Ship(2, onlyVisual=True, transform=Transform((955, 175), angle=-0.9,  parent=self.landParent)),
            Ship(2, onlyVisual=True, transform=Transform((905, 60), angle=-math.pi/2,  parent=self.landParent)),

            Ship(3, onlyVisual=True, transform=Transform((735, 135), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, onlyVisual=True, transform=Transform((875, 80), angle=-math.pi/2,  parent=self.landParent)),
            Ship(3, onlyVisual=True, transform=Transform((620, 80), angle=-2.56,  parent=self.landParent)),

            Ship(4, onlyVisual=True, transform=Transform((765, 150), angle=-math.pi/2,  parent=self.landParent)),
            Ship(4, onlyVisual=True, transform=Transform((823, 143), angle=-math.pi/2,  parent=self.landParent)),

            Ship(5, onlyVisual=True, transform=Transform((700, 120), angle=-1.45,  parent=self.landParent))
        ]
        SceneManager.putInDrawLayer(self.oppositeShips)

        Ship.shipTotal = 10
        Ship.travelDoneCallback = self.__startGame

        self.targetSelector = TargetSelector(
            11,
            self.board1.image.get_rect(center=self.board1.transform.getPosition()),
            self.board2.image.get_rect(center=self.board2.transform.getPosition()),
            Cannon(transform=Transform((50, 40), scale=(0.5, 0.5), parent=self.landParent)),
            Cannon(transform=Transform((980, 120), scale=(-0.5, 0.5), parent=self.landParent)),
            self.__gameEnded
        )
        SceneManager.putInDrawLayer(self.targetSelector)

        self.endGameSign = EndGameSign(transform=Transform.screenCenter())
        SceneManager.putInDrawLayer(self.endGameSign, SceneManager.OVERLAY_LAYER)

        # settings menu stuff
        self.settingsBtn = ImageButton("buttons.settings", transform=Transform((980, 40), scale=(0.7, 0.7)))
        SceneManager.putInDrawLayer(self.settingsBtn, SceneManager.OVERLAY_LAYER)

        self.settings = SettingsSign()
        SceneManager.putInDrawLayer(self.settings, SceneManager.OVERLAY_LAYER)
        self.settingsBtn.setOnClickEvent(self.settings.show)

        


        # amdient stuff
        self.birds = [
            Bird(velocity = 60., transform=Transform(scale=(0.25, 0.25))),
            Bird(velocity = 45., transform=Transform(scale=(0.36, 0.36)))
        ]
        SceneManager.putInDrawLayer(self.birds, SceneManager.SEC_OVERLAY_LAYER)

        self.islands = [
            Diashow([ "ambient.island1", "ambient.island2" ], 0.5, transform=Transform((530, 200), scale=(0.3, 0.3), parent=self.landParent)),
        ]
        SceneManager.putInDrawLayer(self.islands)

        self.shark = Shark(0.3, pygame.Rect(500, 300, 24, 500), (7., 15.), transform=Transform(scale=(0.3, 0.3)))
        SceneManager.putInDrawLayer(self.shark)


    
    def __placementDoneCallback(self):
        Sounds.playSoundEffect("ship_horn")
        for ship in self.oppositeShips:
            ship.doFakeTravel(self.board1.image.get_rect(center=self.board1.transform.getPosition()))
    

    def __startGame(self):
        self.targetSelector.setOwnShipPlacement(self.shipManager.getCurrentShipPlacement())
        self.targetSelector.start()
    
    def __gameEnded(self, won : bool) -> None:
        self.endGameSign.show(won)