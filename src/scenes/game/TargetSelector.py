import re
import pygame
from ai.Difficulties import Difficulties
from ai.StandartGameAI import ShipShape, StandartGameAI
from components.Component import Component
from utils.Animator import Animator
from utils.Images import Sprite
import random
import numpy as np
from utils.Input import Input

from utils.Transform import Transform


class TargetSelector(Component):

    CANNON_BALL_ANIM_TIME = 3.
    
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

        self.cannonBall = Sprite("game.cannon_ball")
        self.cannonBall.enableRoation = True
        self.cannonBall.enableScaling = True
        self.cannonBallScaleAnim = Animator.easeOut(0.2, 0.5, TargetSelector.CANNON_BALL_ANIM_TIME / 2) + Animator.easeIn(0.5, 0.2, TargetSelector.CANNON_BALL_ANIM_TIME / 2)
        self.cannonBallScaleAnim.setHook(lambda s : self.cannonBall.transform.setRelScale((s, s)))
        self.cannonBallRotationAnim = Animator.lerp(0, 75, TargetSelector.CANNON_BALL_ANIM_TIME)
        self.cannonBallRotationAnim.setHook(self.cannonBall.transform.setRelAngle)
        self.cannonBallPositionAnim = None
        self.ownCannon = ownCannon
        self.oppositeCannon = oppositeCannon

    def setOwnShipPlacement(self, shipPlacement : list[ShipShape]) -> None:
        self.ownShipPlacement = shipPlacement
    
    def start(self) -> None:
        if random.random() >= 0.: # TODO: 0.5
            self.doOwnShot()
        else:
            self.doOppositeShot()

    def doOwnShot(self) -> None:
        self.selecting = True
    
    def doOppositeShot(self) -> None:
        pass

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
                    self.fireShot(cell, False)
                    self.hitCells.append(cell)
                    self.selecting = False
                else:
                    self.drawCross = True
                    self.cross.transform.setRelPosition(self.getPosFromCell(cell, self.oppositeBoardRect))
 
    def fireShot(self, cell : tuple[int], byAi : bool):
        startPos = np.array(self.oppositeCannon if byAi else self.ownCannon)
        endPos = np.array(self.getPosFromCell(cell, self.ownBoardRect if byAi else self.oppositeBoardRect))

        def animFun(t : float):
            t /= TargetSelector.CANNON_BALL_ANIM_TIME
            basePos = endPos * t + startPos * (1 - t)
            relExtraHeight = -4 * (t - 0.5)**2 + 1 # just parabola with zeros at 0, 1 and max at 0.5
            return basePos + np.array((0, -relExtraHeight * 70))

        self.cannonBallPositionAnim = Animator(animFun, TargetSelector.CANNON_BALL_ANIM_TIME)
        self.cannonBallPositionAnim.setHook(self.cannonBall.transform.setRelPosition)

        self.cannonBallPositionAnim.play()
        self.cannonBallRotationAnim.play()
        self.cannonBallScaleAnim.play()


    
    def draw(self, screen: pygame.Surface) -> None:
        if self.drawCross:
            self.cross.draw(screen)
        
        if self.cannonBallPositionAnim is not None:
            self.cannonBall.draw(screen)

    

