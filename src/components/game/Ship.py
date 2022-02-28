import random
import pygame
import numpy as np
from ai.ShipShape import ShipShape
from components.ui.AbstractButton import AbstractButton
from components.ui.ImageButton import ImageButton
from utils.Animator import Animator
from utils.Images import Sprite
from utils.Input import Input
from utils.Transform import Transform


class Ship(ImageButton):
    """
    Represents one ship on the board.
    
    Can be clickable or not.
    """

    SCALE = (0.38, 0.3)
    arrivedShips = 0
    shipTotal = 0
    travelDoneCallback = lambda : ...

    MOVEMENT_SPEEDS = {
        2: 40,
        3: 37,
        4: 35,
        5: 30
    }

    ROTATION_SPEEDS = {
        2: 2.5,
        3: 2.0,
        4: 1.7,
        5: 1.5
    }
    

    def __init__(self, length : int, scaleFactor: float = 0.8, onlyVisual : bool = False, transform: Transform = None):
        """
        Constructor of the ship class.

        Args:
            length (int): The length of the ship. [2, 5] is supported.
            scaleFactor (float, optional): How much scales the ship when pressed. Defaults to 0.8.
            onlyVisual (bool, optional): Clickable or not. Defaults to False.
            transform (Transform, optional): The Transform of the component. Defaults to None.
        """
        transform.setRelScale(Ship.SCALE)
        super().__init__(f"game.ships.s{length}", scaleFactor, Input.GAME_LAYER, transform)
        self.__length = length

        if onlyVisual:
            self.disable()

        self.animators = []
    
    def select(self) -> None:
        """
        Should be called when the Ship gets selected.
        """
        self._sprite.image.set_alpha(100)
    
    def deselect(self) -> None:
        """
        Should be called when the another Ship gets selected or the selection process is canceled.
        """
        self._sprite.image.set_alpha(255)
    
    def onEnable(self) -> None:
        self._sprite.image.set_alpha(255)

    def getLength(self) -> int:
        """
        Returns the length of the ship.

        Returns:
            int: The length of the ship.
        """
        return self.__length
    
    def moveToFitShape(self, shape : ShipShape, boardRect : pygame.Rect, boardSize : int, excludeRotation : bool = False) -> None:
        """
        Updates its transform to fit a ShipShape

        Args:
            shape (ShipShape): The shape the ship's position should match.
            boardRect (pygame.Rect): Board width and height.
            boardSize (int): How many rows and cols are on the board.
            excludeRotation (bool, optional): The orientation of the shape should not be included. Defaults to False.
        """
        pos, angle = Ship.getPositionAndRotationFromShape(shape, boardRect, boardSize)
            
        self.transform.setRelPosition(pos)

        if not excludeRotation:
            self.transform.setRelAngle(angle)
            self._sprite.bakeTransform()
        
    @staticmethod
    def getPositionAndRotationFromShape(shape : ShipShape, boardRect : pygame.Rect, boardSize : int) -> tuple[tuple[int], float]:
        """
        Calculates a disired ship's Transform (position and rotation) to match a shape.

        Args:
            shape (ShipShape): The shape the ship's position and roation should match.
            boardRect (pygame.Rect): Board width and height.
            boardSize (int): How many rows and cols are on the board.

        Returns:
            tuple[tuple[int], float]: New position and rotation.
        """
        if shape.orientation == ShipShape.HORIZONTAL:
            y = (shape.cell[1] + 1/2) / boardSize * boardRect.height + boardRect.y
            x = (shape.cell[0] + shape.length / 2) / boardSize * boardRect.width  + boardRect.x
            
        else:
            x = (shape.cell[0] + 1/2) / boardSize * boardRect.width  + boardRect.x
            y = (shape.cell[1] + shape.length / 2) / boardSize * boardRect.height  + boardRect.y
        
        angle = 0 if shape.orientation == ShipShape.HORIZONTAL else -1/2 * np.pi

        return (x, y), angle
    
    def travelTo(self, shape : ShipShape,  boardRect : pygame.Rect, boardSize : int) -> None:
        """
        Starts the ship's travel to a certain shape.

        Happens in the beginning of the game.

        Args:
            shape (ShipShape): Shape where the travel ends.
            boardRect (pygame.Rect):  Board width and height.
            boardSize (int): How many rows and cols are on the board.
        """
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

        # turn gray at the end
        alphaAnim = Animator.const(255., posAnim.getDuration() - 0.5) + Animator.easeIn(255., 130., 0.5)
        alphaAnim.setRepeatMode(Animator.PAUSE)

        # start animations
        self._sprite.enableRoation = True
        self._sprite.bakeTransform(includeRotation=False) # remove prebaked rotation
        self.animators = [ posAnim, angleAnim, alphaAnim ]
        self.animators[0].setHook(self.transform.setRelPosition)
        self.animators[0].play()
        self.animators[1].setHook(self.transform.setRelAngle)
        self.animators[1].play()
        self.animators[2].setHook(self._sprite.image.set_alpha)
        self.animators[2].play()

        # set end hook
        def arriveCallback() -> None:
            self._sprite.enableRoation = False
            self._sprite.bakeTransform()
            self._sprite.image.set_alpha(self.animators[2].get())

            Ship.arrivedShips += 1
            if Ship.travelSquenceDone():
                Ship.travelDoneCallback()

        self.animators[0].setEndCallback(arriveCallback)
    
    def doFakeTravel(self, boardRect : pygame.Rect) -> None:
        """
        Starts the ship's travel to the center of the board. Additionaly the ship disappears while traveling.

        Happens in the beginning of the game for opposite ships.

        Args:
            boardRect (pygame.Rect):  Board width and height.
        """
        rotationSpeed = Ship.ROTATION_SPEEDS[self.__length]
        movementSpeed = Ship.MOVEMENT_SPEEDS[self.__length]

        # Delay
        delay = random.random() * 3.
        posAnim = Animator.const(self.transform.getRelPosition(), delay)
        angleAnim = Animator.const(self.transform.getRelAngle(), delay)
        alphaAnim = Animator.const(255., delay)

        # align vertically
        verticalAngle = - 1/2 * np.pi

        duration = max(abs(self.transform.getRelAngle() - verticalAngle), 0.01) / rotationSpeed
        posAnim += Animator.const(self.transform.getRelPosition(), duration)
        angleAnim += Animator.smoothLerp(self.transform.getRelAngle(), verticalAngle, duration)
        alphaAnim += Animator.const(255., duration)

        # move
        endPos = np.array([self.transform.getRelPosition()[0], boardRect.y + boardRect.height / 2])

        duration = max(abs(self.transform.getRelPosition()[1] - endPos[1]), 0.01) / movementSpeed
        posAnim += Animator.smoothLerp(self.transform.getRelPosition(), endPos, duration)
        angleAnim += Animator.const(verticalAngle, duration)
        alphaAnim += Animator.const(255., duration / 4) + Animator.easeIn(255., 0., duration / 4)

        # start animations
        self._sprite.enableRoation = True
        self._sprite.bakeTransform(includeRotation=False) # remove prebaked rotation
        self.animators = [ posAnim, angleAnim, alphaAnim ]
        self.animators[0].setHook(self.transform.setRelPosition)
        self.animators[0].play()
        self.animators[1].setHook(self.transform.setRelAngle)
        self.animators[1].play()
        self.animators[2].setHook(self._sprite.image.set_alpha)
        self.animators[2].play()


    
    @staticmethod
    def travelSquenceDone() -> bool:
        """
        Returns whether all ships have arrived.

        Returns:
            bool: If all ships have arrived.
        """
        return Ship.arrivedShips >= Ship.shipTotal
