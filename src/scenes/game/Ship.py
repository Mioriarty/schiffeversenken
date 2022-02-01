from numpy import angle
from ai.StandartGameAI import ShipShape
from components.Component import Component
from components.ui.ImageButton import ImageButton
from utils.Images import Sprite
from utils.Transform import Transform
import pygame
import functools
import math


class Ship(ImageButton):

    SCALE = (0.38, 0.3)
    def __init__(self, length : int, scaleFactor: float = 0.8, transform: Transform = None):
        transform.setRelScale(Ship.SCALE)
        super().__init__(Sprite(f"game.ships.s{length}"), scaleFactor, transform)
        self.__length = length
    
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
        
        angle = 0 if shape.orientation == ShipShape.HORIZONTAL else -1/2 * math.pi

        return (x, y), angle

    

class ShipManager(Component):

    
    def __init__(self, ships : list[Ship], boardRect : pygame.Rect, boardSize : int):
        super().__init__(None)
        print(boardRect)

        self.ships = ships
        self.selectedIndex = -1
        self.boardRect = boardRect
        self.boardSize = boardSize
        self.hoverOrientation = ShipShape.HORIZONTAL
        self.hoverSprite = None

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

    

    def draw(self, screen: pygame.Surface) -> None:
        for ship in self.ships:
            ship.draw(screen)
        
        for shipShape, ship in self.placedShips:
            if shipShape.orientation != -1:
                ship.draw(screen)
        
        if self.selectedIndex > -1 and self.boardRect.collidepoint(pygame.mouse.get_pos()):
            self.hoverSprite.draw(screen)

    
    def update(self, dt: float) -> None:
        if self.selectedIndex > -1 and self.boardRect.collidepoint(pygame.mouse.get_pos()):
            hoverLength = self.ships[self.selectedIndex].getLength()

            if pygame.event.peek(pygame.MOUSEWHEEL):
                self.hoverOrientation = (self.hoverOrientation + 1) % 2
            
            cell = self.getPlacementCell(hoverLength)

            hoverShape = ShipShape(hoverLength, cell, self.hoverOrientation)
            isValidHoverPos = hoverShape.fitsInShipPlacement([s[0] for s in self.placedShips])

            pos, angle = Ship.getPositionAndRotationFromShape(hoverShape, self.boardRect, self.boardSize)
            self.hoverSprite.transform.setRelPosition(pos)
            self.hoverSprite.image.set_alpha(255 if isValidHoverPos else 100)

            if pygame.event.peek(pygame.MOUSEWHEEL):
                self.hoverSprite.transform.setRelAngle(angle)
                self.hoverSprite.bakeTransform()
            
            elif isValidHoverPos and pygame.event.peek(pygame.MOUSEBUTTONUP):
                self.placeShip(cell)

                
    def getPlacementCell(self, shipLength : int) -> tuple[int]:
        cell = ((pygame.mouse.get_pos()[0] - self.boardRect.x) * self.boardSize // self.boardRect.width,
                (pygame.mouse.get_pos()[1] - self.boardRect.y) * self.boardSize // self.boardRect.height )

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