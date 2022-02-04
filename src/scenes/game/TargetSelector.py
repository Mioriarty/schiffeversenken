import re
import pygame
from ai.Difficulties import Difficulties
from ai.StandartGameAI import ShipShape, StandartGameAI
from components.Component import Component
from components.game.CannonBall import CannonBall
from components.game.Fire import Fire
from scenes.Scene import SceneManager
from utils.Images import Sprite
import random
import numpy as np
from utils.Input import Input

from utils.Transform import Transform


class TargetSelector(Component):

    CANNON_BALL_ANIM_TIME = 2.
    
    def __init__(self, boardSize : int, ownBoardRect : pygame.Rect, oppositeBoardRect : pygame.Rect, ownCannon : tuple[float], oppositeCannon : tuple[float]):
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
        self.ownCannon = ownCannon
        self.oppositeCannon = oppositeCannon
        self.aiTurn = False

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
        startPos = self.oppositeCannon if self.aiTurn else self.ownCannon
        endPos = self.getPosFromCell(cell, self.ownBoardRect if self.aiTurn else self.oppositeBoardRect)
        hit = ShipShape.cellInPlacement(cell, self.ownShipPlacement if self.aiTurn else self.oppositeShipPlacement)

        self.cannonBall.fire(startPos, endPos, hit)
    
    def shotAnimationFinished(self, pos : tuple[float], hit : bool) -> None:
        if hit:
            def createFire():
                self.fires.append(Fire(transform=Transform(pos, scale=(0.4, 0.4))))
            
            SceneManager.requestComponent(createFire)

        if self.aiTurn:
            self.doOwnShot()
        else:
            self.doOppositeShot()

    def draw(self, screen: pygame.Surface) -> None:
        if self.drawCross:
            self.cross.draw(screen)
        
        self.cannonBall.draw(screen)

        for fire in self.fires:
            fire.draw(screen)

    

