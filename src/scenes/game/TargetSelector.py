import re
from typing import Callable
import pygame
from ai.Difficulties import Difficulties
from ai.StandartGameAI import ShipShape, StandartGameAI, printBoard
from components.Component import Component
from components.game.Cannon import Cannon
from components.game.CannonBall import CannonBall
from components.game.Fire import Fire
from scenes.Scene import SceneManager
from utils.Images import Sprite
import random
import numpy as np
from utils.Input import Input

from utils.Transform import Transform


class TargetSelector(Component):

    TOTAL_SHIP_TILES = 5 * 1 + 4 * 2 + 3 * 3 + 2 * 4
    
    def __init__(self, boardSize : int, ownBoardRect : pygame.Rect, oppositeBoardRect : pygame.Rect, ownCannon : Cannon, oppositeCannon : Cannon, gameEndCallback : Callable[[bool], None]):
        super().__init__(None)
        self.boardSize = boardSize
        self.ownBoardRect = ownBoardRect
        self.oppositeBoardRect = oppositeBoardRect
        self.ownShipPlacement = []
        self.ai = StandartGameAI(boardSize, boardSize, Difficulties.getSelectedChanceOfMistake())
        self.oppositeShipPlacement = self.ai.getShipPlacement()
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
        self.ownShipPlacement = shipPlacement
    
    def start(self) -> None:
        if random.random() >= 0.5:
            self.doOwnShot()
        else:
            self.doOppositeShot()

    def doOwnShot(self) -> None:
        self.aiTurn = False
        self.selecting = True
    
    def doOppositeShot(self) -> None:
        self.aiTurn = True
        cell = self.ai.getNextShot()
        cellState = StandartGameAI.SHIP if ShipShape.cellInPlacement(cell, self.ownShipPlacement) else StandartGameAI.CHECKED_NO_SHIP
        self.ai.submitInfo(cell, cellState)

        self.fireShot(cell)

    def getCellFromMousePos(self, boardRect : pygame.Rect) -> tuple[int]:
        return ((Input.getMousePos()[0] - boardRect.x) * self.boardSize // boardRect.width,
                (Input.getMousePos()[1] - boardRect.y) * self.boardSize // boardRect.height )
    
    def getPosFromCell(self, cell : tuple[int], boardRect : pygame.Rect) -> tuple[float]:
        return ((cell[0] + 1/2) / self.boardSize * boardRect.width  + boardRect.x, 
                (cell[1] + 1/2) / self.boardSize * boardRect.height + boardRect.y)


    def update(self, dt: float) -> None:
        self.drawCross = False

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
        if self.aiTurn:
            startPos = self.oppositeCannon.getOpeningPos()
            self.oppositeCannon.animation.play()
            endPos = self.getPosFromCell(cell, self.ownBoardRect)
            hit = ShipShape.cellInPlacement(cell, self.ownShipPlacement)
            printBoard(self.ai.board, 11, 11)
            print(self.ai.numShips)
            print()
        else:
            startPos = self.ownCannon.getOpeningPos()
            self.ownCannon.animation.play()
            endPos = self.getPosFromCell(cell, self.oppositeBoardRect)
            hit = ShipShape.cellInPlacement(cell, self.oppositeShipPlacement)

        self.cannonBall.fire(startPos, endPos, hit)
    
    def shotAnimationFinished(self, pos : tuple[float], hit : bool) -> None:
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

    

