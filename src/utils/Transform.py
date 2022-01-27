from doctest import ELLIPSIS_MARKER
import numpy as np

class Transform:

    @staticmethod
    def calcRotationMatrix(angle : float) -> np.ndarray:
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([ [ c, -s ], [ s, c ] ])

    def __init__(self, position : tuple | list | np.ndarray = (0., 0.), angle : float = 0., scale : tuple | list | np.ndarray = (1., 1.), parent : 'Transform' = None):
        self.__position : np.ndarray = np.array(position)
        self.__angle : float         = angle
        self.__scale  : np.ndarray   = np.array(scale)
        self.__parent : 'Transform'  = parent
    
    @classmethod
    def fromTransform(self, other : 'Transform') -> 'Transform':
        if other is None:
            return Transform()
        else:
            return Transform(other.__position, other.__angle, other.__scale, other.__parent)
    

    def getPosition(self) -> np.ndarray:
        if self.__parent == None:
            return self.__position
        return self.__parent.apply(self.__position)

    def getAngle(self) -> float:
        if self.__parent == None:
            return self.__angle
        return self.__angle + self.__parent.getAngle()
    
    def getScale(self) -> np.ndarray:
        if self.__parent == None:
            return self.__scale
        return self.__scale * self.__parent.getScale()
    
    def getRelPosition(self) -> np.ndarray:
        return self.__position
    
    def getRelAngle(self) -> float:
        return self.__angle

    def getRelScale(self) -> np.ndarray:
        return self.__scale

    def translate(self, offset : tuple | list | np.ndarray) -> None:
        self.__position += np.array(offset)
    
    def rotate(self, angleOffset : float) -> None:
        self.__angle += angleOffset
    
    def scale(self, factor : float | tuple | list | np.ndarray) -> None:
        if isinstance(factor, list) or isinstance(factor, tuple):
            factor = np.array(factor)
        self.__scale *= factor
    
    def setRelPosition(self, position : tuple | list | np.ndarray) -> None:
        self.__position = np.array(position)
    
    def setRelXPos(self, xPos : float) -> None:
        self.__position[0] = xPos
    
    def setRelYPos(self, yPos : float) -> None:
        self.__position[1] = yPos
    
    def setRelAngle(self, angle : float) -> None:
        self.__angle = angle

    def setRelScale(self, scale : tuple | list | np.ndarray) -> None:
        self.__scale = np.array(scale)
    
    def setRelXScale(self, xScale : float) -> None:
        self.__scale[0] = xScale
    
    def setRelYScale(self, yScale : float) -> None:
        self.__scale[1] = yScale
    
    def setParent(self, parent : 'Transform') -> None:
        self.__parent = parent

    def apply(self, vector : tuple | list | np.ndarray) -> np.ndarray:
        return np.matmul(Transform.calcRotationMatrix(self.getAngle()), np.array(vector) * self.getScale()) + self.getPosition()

    def applyMultiple(self, vectors : tuple | list) -> list[np.ndarray]:
        return [ self.apply(v) for v in vectors ]
    
    def applyInv(self, vector : tuple | list | np.ndarray) -> np.ndarray :
        return np.matmul(Transform.calcRotationMatrix(-self.getAngle()), np.array(vector) - self.getPosition()) / self.getScale()
    
    def applyInvMultiple(self, vectors : tuple | list) -> list[np.ndarray]:
        return [ self.applyInv(v) for v in vectors ]
    
    @classmethod
    def screenCenter(cls, x : float = None, y : float = None, angle : float = 0.0, scale : tuple | list | np.ndarray = (1.0, 1.0), parent : 'Transform' = None):
        return cls((512. if x is None else x, 384. if y is None else y), angle, scale, parent)