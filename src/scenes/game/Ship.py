import random
from ai.StandartGameAI import ShipShape
from components.Component import Component
from components.ui.ImageButton import ImageButton
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Input import Input
from utils.Transform import Transform
import pygame
import functools
import numpy as np


class Ship(ImageButton):

    SCALE = (0.38, 0.3)
    arrivedShips = 0
    shipTotal = 0

    MOVEMENT_SPEEDS = {
        2: 40,
        3: 37,
        4: 35,
        5: 22
    }

    ROTATION_SPEEDS = {
        2: 2.5,
        3: 2.0,
        4: 1.7,
        5: 1.5
    }
    

    def __init__(self, length : int, scaleFactor: float = 0.8, transform: Transform = None):
        transform.setRelScale(Ship.SCALE)
        super().__init__(Sprite(f"game.ships.s{length}"), scaleFactor, transform)
        self.__length = length

        self.animators = []
    
    def select(self) -> None:
        self._sprite.image.set_alpha(100)
    
    def deselect(self) -> None:
        self._sprite.image.set_alpha(255)
    
    def onEnable(self) -> None:
        self._sprite.image.set_alpha(255)

    def getLength(self) -> int:
        return self.__length
    
    def moveToFitShape(self, shape : ShipShape, boardRect : pygame.Rect, boardSize : int, excludeRotation : bool = False) -> None:
        pos, angle = Ship.getPositionAndRotationFromShape(shape, boardRect, boardSize)
            
        self.transform.setRelPosition(pos)

        if not excludeRotation:
            self.transform.setRelAngle(angle)
            self._sprite.bakeTransform()
        
    @staticmethod
    def getPositionAndRotationFromShape(shape : ShipShape, boardRect : pygame.Rect, boardSize : int):
        if shape.orientation == ShipShape.HORIZONTAL:
            y = (shape.cell[1] + 1/2) / boardSize * boardRect.height + boardRect.y
            x = (shape.cell[0] + shape.length / 2) / boardSize * boardRect.width  + boardRect.x
            
        else:
            x = (shape.cell[0] + 1/2) / boardSize * boardRect.width  + boardRect.x
            y = (shape.cell[1] + shape.length / 2) / boardSize * boardRect.height  + boardRect.y
        
        angle = 0 if shape.orientation == ShipShape.HORIZONTAL else -1/2 * np.pi

        return (x, y), angle
    
    def travelTo(self, shape : ShipShape,  boardRect : pygame.Rect, boardSize : int):
        pos, _ = Ship.getPositionAndRotationFromShape(shape, boardRect, boardSize)

        rotationSpeed = Ship.ROTATION_SPEEDS[self.__length]
        movementSpeed = Ship.MOVEMENT_SPEEDS[self.__length]

        # make ships that have to travel far quicker
        movementSpeed += 15 * ((pos[1] - boardRect.y) / float(boardRect.height))
        
        # Delay
        delay = random.random() * 3.
        posAnim = Animator.const(self.transform.getRelPosition(), delay)
        angleAnim = Animator.const(self.transform.getRelAngle(), delay)

        # align vertically
        verticalAngle =  - 1/2 * np.pi

        duration = max(abs(self.transform.getRelAngle() - verticalAngle), 0.01) / rotationSpeed
        posAnim += Animator.const(self.transform.getRelPosition(), duration)
        angleAnim += Animator.smoothLerp(self.transform.getRelAngle(), verticalAngle, duration)

        # vertical movement
        verticalEndPos = np.array([self.transform.getRelPosition()[0], pos[1]])

        duration = max(abs(self.transform.getRelPosition()[1] - pos[1]), 0.01) / movementSpeed
        posAnim += Animator.smoothLerp(self.transform.getRelPosition(), verticalEndPos, duration)
        angleAnim += Animator.const(verticalAngle, duration)

        # align horizontally
        horizontalAngle = 0 if verticalEndPos[0] < pos[0] else - np.pi

        duration = max(abs(verticalAngle - horizontalAngle), 0.01) / rotationSpeed
        posAnim += Animator.const(verticalEndPos, duration)
        angleAnim += Animator.smoothLerp(verticalAngle, horizontalAngle, duration)

        # horizontal movement
        duration = max(abs(verticalEndPos[0] - pos[0]), 0.01) / movementSpeed
        posAnim += Animator.smoothLerp(verticalEndPos, np.array(pos), duration)
        angleAnim += Animator.const(horizontalAngle, duration)

        # rotate to match oprientation in necessary
        if shape.orientation == ShipShape.VERTICAL:
            finalAngle = - 1/2 * np.pi

            duration = max(abs(horizontalAngle - finalAngle), 0.01) / rotationSpeed
            posAnim += Animator.const(pos, duration)
            angleAnim += Animator.smoothLerp(horizontalAngle, finalAngle, duration)



        # start animations
        self._sprite.enableRoation = True
        self._sprite.bakeTransform(includeRotation=False) # remove prebaked rotation
        self.animators = [ posAnim, angleAnim ]
        self.animators[0].setHook(self.transform.setRelPosition)
        self.animators[0].play()
        self.animators[1].setHook(self.transform.setRelAngle)
        self.animators[1].play()

        # set end hook
        def arriveCallback() -> None:
            Ship.arrivedShips += 1
            self._sprite.enableRoation = False
            self._sprite.bakeTransform()

        self.animators[0].setEndCallback(arriveCallback)

    
    @staticmethod
    def travelSquenceDone() -> bool:
        return Ship.arrivedShips >= Ship.shipTotal

class ShipPlacer(Component):

    
    def __init__(self, ships : list[Ship], startBtn : ImageButton, boardRect : pygame.Rect, boardSize : int):
        super().__init__(None)

        self.ships = ships
        self.startBtn = startBtn
        self.startBtn.disable()
        self.startBtn.setOnClickEvent(self.startGame)
        self.selectedIndex = -1
        self.boardRect = boardRect
        self.boardSize = boardSize
        self.hoverOrientation = ShipShape.HORIZONTAL
        self.hoverSprite = None
        self.placementDone = False
        self.inGame = False

        self.placedShips = [ [ShipShape(s.getLength(), (-1, -1), -1), Ship(s.getLength(), transform=Transform(scale=Ship.SCALE))] for s in self.ships ]

        for i in range(len(ships)):
            self.ships[i].setOnClickEvent(functools.partial(self.__clickOnShip, i))
            self.placedShips[i][1].setOnClickEvent(functools.partial(self.__removeShip, i))
        
        
    

    def __clickOnShip(self, index : int) -> None:
        if self.selectedIndex > -1:
            self.ships[self.selectedIndex].deselect()
        
        self.selectedIndex = index
        self.ships[self.selectedIndex].select()
        self.hoverOrientation = ShipShape.HORIZONTAL
        length = self.ships[index].getLength()
        self.hoverSprite = Sprite(f"game.ships.s{length}", transform=Transform(scale=Ship.SCALE), bakeNow=True)
    
    def __removeShip(self, index : int) -> None:
        length = self.placedShips[index][0].length
        self.placedShips[index][0] = ShipShape(length, (-1, -1), -1)
        self.placedShips[index][1].disable()
        self.ships[index].enable()

        self.placementDone = False
        self.startBtn.disable()
    

    def draw(self, screen: pygame.Surface) -> None:
        for ship in self.ships:
            ship.draw(screen)
        
        if not self.inGame:
            for shipShape, ship in self.placedShips:
                if shipShape.orientation != -1:
                    ship.draw(screen)
        
        if self.selectedIndex > -1 and self.boardRect.collidepoint(Input.getMousePos()):
            self.hoverSprite.draw(screen)
        
        if self.placementDone:
            self.startBtn.draw(screen)

    
    def update(self, dt: float) -> None:
        if self.selectedIndex > -1 and self.boardRect.collidepoint(Input.getMousePos()):
            hoverLength = self.ships[self.selectedIndex].getLength()

            mouseEvent = Input.getEvent(pygame.MOUSEBUTTONUP)
            if mouseEvent is not None and (4 <= mouseEvent.button <= 5):
                self.hoverOrientation = (self.hoverOrientation + 1) % 2
            
            cell = self.getPlacementCell(hoverLength)

            hoverShape = ShipShape(hoverLength, cell, self.hoverOrientation)
            isValidHoverPos = hoverShape.fitsInShipPlacement([s[0] for s in self.placedShips])

            pos, angle = Ship.getPositionAndRotationFromShape(hoverShape, self.boardRect, self.boardSize)
            self.hoverSprite.transform.setRelPosition(pos)
            self.hoverSprite.image.set_alpha(255 if isValidHoverPos else 100)

            if mouseEvent is not None and (4 <= mouseEvent.button <= 5):
                self.hoverSprite.transform.setRelAngle(angle)
                self.hoverSprite.bakeTransform()
            
            elif isValidHoverPos and mouseEvent is not None and mouseEvent.button == 1:
                self.placeShip(cell)
        
        print(Ship.travelSquenceDone())

                
    def getPlacementCell(self, shipLength : int) -> tuple[int]:
        cell = ((Input.getMousePos()[0] - self.boardRect.x) * self.boardSize // self.boardRect.width,
                (Input.getMousePos()[1] - self.boardRect.y) * self.boardSize // self.boardRect.height )

        if self.hoverOrientation == ShipShape.HORIZONTAL:
            # only modify xCoord
            xCoord = cell[0] - shipLength // 2
            xCoord = max(0, min(xCoord, self.boardSize - shipLength))
            return (xCoord, cell[1])
        
        else:
            # only modify yCoord
            yCoord = cell[1] - shipLength // 2
            yCoord = max(0, min(yCoord, self.boardSize - shipLength))
            return (cell[0], yCoord)
        

    def placeShip(self, cell : tuple[int]) -> None:
        length = self.ships[self.selectedIndex].getLength()
        shape = ShipShape(length, cell, self.hoverOrientation)

        self.placedShips[self.selectedIndex][0] = shape
        self.placedShips[self.selectedIndex][1].moveToFitShape(shape, self.boardRect, self.boardSize)
        self.placedShips[self.selectedIndex][1].enable()

        self.ships[self.selectedIndex].disable()
        self.selectedIndex = -1

        self.placementDone = all(s[0].orientation != -1 for s in self.placedShips)
        if self.placementDone:
            self.startBtn.enable()
    
    def startGame(self) -> None:
        self.inGame = True

        for (shipShape, placedShip), outsideShip in zip(self.placedShips, self.ships):
            placedShip.disable()
            outsideShip.disable()
            outsideShip.deselect()

            outsideShip.travelTo(shipShape, self.boardRect, self.boardSize)

        
