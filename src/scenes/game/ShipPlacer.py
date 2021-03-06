from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
from components.Component import Component
from components.game.Ship import Ship
from components.ui.ImageButton import ImageButton
from utils.Images import Sprite
from utils.Input import Input
from utils.Sounds import Sounds
from utils.Transform import Transform
import pygame
import functools

class ShipPlacer(Component):
    """
    Represents the first phase of the game. Here the ship placing happens.
    """

    
    def __init__(self, ships : list[Ship], startBtn : ImageButton, boardRect : pygame.Rect, boardSize : int):
        """
        Constructor of the ShipPlacer class.

        Args:
            ships (list[Ship]): How many ships of which length are in the game. The key is the length of the ships and values is the number of that kind of ships.
            startBtn (ImageButton): ImageButton that appears when the placment is done. When clicked this game phase stops.
            boardRect (pygame.Rect): Rect of the own board.
            boardSize (int): How many rows and columns does the board have.
        """
        super().__init__(None)

        self.ships = ships
        self.startBtn = startBtn
        self.startBtn.disable()
        self.startBtn.addOnClickEvent(self.startGame)
        self.selectedIndex = -1
        self.boardRect = boardRect
        self.boardSize = boardSize
        self.hoverOrientation = ShipShape.HORIZONTAL
        self.hoverSprite = None
        self.placementDone = False
        self.inGame = False

        self.placedShips = [ [ShipShape(s.getLength(), (-1, -1), -1), Ship(s.getLength(), transform=Transform(scale=Ship.SCALE), onlyVisual=True)] for s in self.ships ]

        for i in range(len(ships)):
            self.ships[i].setOnClickEvent(functools.partial(self.__clickOnShip, i))
            self.placedShips[i][1].setOnClickEvent(functools.partial(self.__removeShip, i))
        
        
    

    def __clickOnShip(self, index : int) -> None:
        """
        Gets called when a ship on the side is selected.

        Args:
            index (int): Index in the self.ships list in which the clicked ship is.
        """
        if self.selectedIndex > -1:
            self.ships[self.selectedIndex].deselect()
        
        self.selectedIndex = index
        self.ships[self.selectedIndex].select()
        self.hoverOrientation = ShipShape.HORIZONTAL
        length = self.ships[index].getLength()
        self.hoverSprite = Sprite(f"game.ships.s{length}", transform=Transform(scale=Ship.SCALE), bakeNow=True)
    
    def __removeShip(self, index : int) -> None:
        """
        Gets called when a ship in the board is clicked. It will be removed.

        Args:
            index (int): Index in the self.placedShips list in which the clicked ship is.
        """
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
        
        if self.placementDone and not self.inGame:
            self.startBtn.draw(screen)

    
    def update(self, dt: float) -> None:
        if not Input.checkInputLayer(Input.GAME_LAYER):
            return

        mouseEvent = Input.getEvent(pygame.MOUSEBUTTONUP)
        if mouseEvent is not None and mouseEvent.button == 3:
            # cancel ship placement on left click
            if self.selectedIndex > -1:
                self.ships[self.selectedIndex].deselect()
                self.selectedIndex = -1

        elif self.selectedIndex > -1 and self.boardRect.collidepoint(Input.getMousePos()):
            hoverLength = self.ships[self.selectedIndex].getLength()

            if mouseEvent is not None and (4 <= mouseEvent.button <= 5):
                self.hoverOrientation = (self.hoverOrientation + 1) % 2
            
            cell = self.getPlacementCell(hoverLength)

            hoverShape = ShipShape(hoverLength, cell, self.hoverOrientation)
            isValidHoverPos = ShipPlacement(self.getCurrentShipPlacement()).fitsIn(hoverShape)

            pos, angle = Ship.getPositionAndRotationFromShape(hoverShape, self.boardRect, self.boardSize)
            self.hoverSprite.transform.setRelPosition(pos)
            self.hoverSprite.image.set_alpha(255 if isValidHoverPos else 100)

            if mouseEvent is not None and (4 <= mouseEvent.button <= 5):
                self.hoverSprite.transform.setRelAngle(angle)
                self.hoverSprite.bakeTransform()
            
            elif isValidHoverPos and mouseEvent is not None and mouseEvent.button == 1:
                self.placeShip(cell)
        

                
    def getPlacementCell(self, shipLength : int) -> tuple[int]:
        """
        Calculates based on the mouseposition and the ship length which should be the ships position

        Args:
            shipLength (int): The length of the currently selected ship.

        Returns:
            tuple[int]: The position of that ship.
        """
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
        """
        Places the selected ship at a certain position.

        Args:
            cell (tuple[int]): At what position the selected ship should be placed.-
        """
        length = self.ships[self.selectedIndex].getLength()
        shape = ShipShape(length, cell, self.hoverOrientation)

        self.placedShips[self.selectedIndex][0] = shape
        self.placedShips[self.selectedIndex][1].moveToFitShape(shape, self.boardRect, self.boardSize)
        self.placedShips[self.selectedIndex][1].enable()

        self.ships[self.selectedIndex].disable()
        self.selectedIndex = -1

        self.placementDone = all(s[0].orientation != -1 for s in self.placedShips)

        Sounds.playSoundEffect("click")

        if self.placementDone:
            self.startBtn.enable()
    
    def startGame(self) -> None:
        """
        Gets called when the Button to start playing is pressed.

        It will kick off the ship travels of the own ships.
        """
        self.inGame = True
        self.startBtn.disable()

        for (shipShape, placedShip), outsideShip in zip(self.placedShips, self.ships):
            placedShip.disable()
            outsideShip.disable()

            outsideShip.travelTo(shipShape, self.boardRect, self.boardSize)
    
    def getCurrentShipPlacement(self) -> list[Ship]:
        """
        Returns the placement containing all currently placed ships.

        Returns:
            list[Ship]: The placement containing all currently placed ships.
        """
        return [ s[0] for s in self.placedShips if s[0].orientation != -1]

        
