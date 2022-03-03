from typing import Callable
import pygame
from ai.AiMaster import AiMaster
from ai.Board import Board
from ai.Difficulties import Difficulties
from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
from components.Component import Component
from components.game.Cannon import Cannon
from components.game.CannonBall import CannonBall
from components.game.Fire import Fire
from scenes.Scene import SceneManager
from utils.Images import Sprite
import random
from utils.Input import Input

from utils.Transform import Transform


class TargetSelector(Component):
    """
    Represents the second phase of the game. Here the shoting happens.
    """

    TOTAL_SHIP_TILES = 5 * 1 + 4 * 2 + 3 * 3 + 2 * 4
    
    def __init__(self, boardSize : int, ownBoardRect : pygame.Rect, oppositeBoardRect : pygame.Rect, ownCannon : Cannon, oppositeCannon : Cannon, gameEndCallback : Callable[[bool], None]):
        """
        Constructor of the TargetSelector class.

        Args:
            boardSize (int): How many rows and columns does the board have.
            ownBoardRect (pygame.Rect): The rectangle on the screen of the players board.
            oppositeBoardRect (pygame.Rect):  The rectangle on the screen of the compouters board.
            ownCannon (Cannon): The player's cannon.
            oppositeCannon (Cannon): The computer's cannon.
            gameEndCallback (Callable[[bool], None]): Callback that gets called when the game ended. The parameter specifies whether the player won or not.
        """
        super().__init__(None)
        self.boardSize = boardSize
        self.ownBoardRect = ownBoardRect
        self.oppositeBoardRect = oppositeBoardRect
        self.ownShipPlacement = []
        self.ai = AiMaster(boardSize, boardSize, Difficulties.getSelectedChanceOfMistake(), Difficulties.getSelectedNumShipPlacementTries(), Difficulties.doesSelecteduseProAi())
        self.oppositeShipPlacement = None
        self.selecting = False
        self.cross = Sprite("game.cross", transform=Transform(scale=(0.5, 0.5)), bakeNow=True)
        self.hitCells = []
        self.drawCross = False
        self.cannonBall = CannonBall(self.shotAnimationFinished)
        self.fires = []
        self.flags = []
        self.ownCannon = ownCannon
        self.oppositeCannon = oppositeCannon
        self.aiTurn = False
        self.gameEndcallback = gameEndCallback
        self.playerFoundShipTiles = 0
        self.aiFoundShipTiles     = 0

    def setOwnShipPlacement(self, shipPlacement : list[ShipShape]) -> None:
        """
        Sets the player's ship placement.

        This will propably be called when the ship placing phase has ended.

        Args:
            shipPlacement (list[ShipShape]): The player's ship placement.
        """
        self.ownShipPlacement = ShipPlacement(shipPlacement)
    
    def start(self) -> None:
        """
        Kicks off this game phase and thus initiates the first shot.

        Whether the computer or player starts will be randomly selected with equal odds.
        """
        self.oppositeShipPlacement = self.ai.generateShipPlacement()
        if random.random() >= 0.5:
            self.doOwnShot()
        else:
            self.doOppositeShot()

    def doOwnShot(self) -> None:
        """
        Executes a player's shot.

        This means that the tile selection can start.
        """
        self.aiTurn = False
        self.selecting = True
    
    def doOppositeShot(self) -> None:
        """
        Executes a computer's shot.

        The computer will shoot immediatly.
        """
        self.aiTurn = True
        cell = self.ai.getNextShot()
        cellState = Board.SHIP if self.ownShipPlacement.cellOccupied(cell) else Board.CHECKED_NO_SHIP
        self.ai.submitInfo(cell, cellState)

        self.fireShot(cell)

    def getCellFromMousePos(self, boardRect : pygame.Rect) -> tuple[int]:
        """
        Returns the hovered cell for a certain board rect and a mouse position.

        Args:
            boardRect (pygame.Rect): The board rect to use.

        Returns:
            tuple[int]: The hovered cell in the specified board rect.
        """
        return ((Input.getMousePos()[0] - boardRect.x) * self.boardSize // boardRect.width,
                (Input.getMousePos()[1] - boardRect.y) * self.boardSize // boardRect.height )
    
    def getPosFromCell(self, cell : tuple[int], boardRect : pygame.Rect) -> tuple[float]:
        """
        Returns the center screen coordinates for a cell in a board rect.

        Args:
            cell (tuple[int]): The cell of which you want to get the screen coordinates from.
            boardRect (pygame.Rect): The board rect where the cell is in.

        Returns:
            tuple[float]: The center screen coordinates for the specified cell in the specified board rect.
        """
        return ((cell[0] + 1/2) / self.boardSize * boardRect.width  + boardRect.x, 
                (cell[1] + 1/2) / self.boardSize * boardRect.height + boardRect.y)


    def update(self, dt: float) -> None:
        self.drawCross = False

        if not Input.checkInputLayer(Input.GAME_LAYER):
            return

        if self.selecting and self.oppositeBoardRect.collidepoint(Input.getMousePos()):
            cell = self.getCellFromMousePos(self.oppositeBoardRect)
            
            if cell not in self.hitCells:
                if Input.hasEvent(pygame.MOUSEBUTTONUP) and Input.getEvent(pygame.MOUSEBUTTONUP).button == 1:
                    self.fireShot(cell)
                    self.hitCells.append(cell)
                    self.selecting = False
                else:
                    self.drawCross = True
                    self.cross.transform.setRelPosition(self.getPosFromCell(cell, self.oppositeBoardRect))
 
    def fireShot(self, cell : tuple[int]):
        """
        Executes all the animations and logic to be done during a shot.

        Args:
            cell (tuple[int]): Destination cell of the shot.
        """
        if self.aiTurn:
            startPos = self.oppositeCannon.getOpeningPos()
            self.oppositeCannon.animation.play()
            endPos = self.getPosFromCell(cell, self.ownBoardRect)
            hit = self.ownShipPlacement.cellOccupied(cell)

            self.ai.printState()
        else:
            startPos = self.ownCannon.getOpeningPos()
            self.ownCannon.animation.play()
            endPos = self.getPosFromCell(cell, self.oppositeBoardRect)
            hit = self.oppositeShipPlacement.cellOccupied(cell)

        self.cannonBall.fire(startPos, endPos, hit)
    
    def shotAnimationFinished(self, pos : tuple[float], hit : bool) -> None:
        """
        Callback that gets called when the shot graphics are done. It placed a flag or a fire and kicks off the next shot.

        Args:
            pos (tuple[float]): Screen position where the shot hit.
            hit (bool): Whether the shot hit a ship.
        """
        if hit:
            def createFire():
                self.fires.append(Fire(transform=Transform(pos, scale=(0.4, 0.4))))
            
            SceneManager.requestComponent(createFire)

            # check whether game ended
            if self.aiTurn:
                self.aiFoundShipTiles += 1
                if self.aiFoundShipTiles == TargetSelector.TOTAL_SHIP_TILES:
                    self.gameEndcallback(False)
                    return
            
            else:
                self.playerFoundShipTiles += 1
                if self.playerFoundShipTiles == TargetSelector.TOTAL_SHIP_TILES:
                    self.gameEndcallback(True)
                    return
        
        else:
            def createFlag():
                self.flags.append(Sprite("game.flag", transform=Transform(pos, scale=(0.4, 0.4)), bakeNow=True))
            
            SceneManager.requestComponent(createFlag)

        if self.aiTurn:
            self.doOwnShot()
        else:
            self.doOppositeShot()

    def draw(self, screen: pygame.Surface) -> None:
        if self.drawCross:
            self.cross.draw(screen)
        
        self.cannonBall.draw(screen)
        self.ownCannon.draw(screen)
        self.oppositeCannon.draw(screen)

        for fire in self.fires:
            fire.draw(screen)
        
        for flag in self.flags:
            flag.draw(screen)

    

