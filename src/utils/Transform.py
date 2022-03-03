from doctest import ELLIPSIS_MARKER
import numpy as np

class Transform:
    """
    Represents a position, rotation and scale in 2d for a component. 

    Multiple components can be chained together as parents and childs. Than the childs position, rotation and scale are relative to the parent ones.
    """

    @staticmethod
    def __calcRotationMatrix(angle : float) -> np.ndarray:
        """
        Claulates a 2x2 rotation matrix for a given angle

        Args:
            angle (float): The angle, the matrix should encode.

        Returns:
            np.ndarray: The resulting matrix.
        """
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([ [ c, -s ], [ s, c ] ])

    def __init__(self, position : tuple | list | np.ndarray = (0., 0.), angle : float = 0., scale : tuple | list | np.ndarray = (1., 1.), parent : 'Transform' = None):
        """
        Constructor of the Transfrom class.

        Args:
            position (tuple | list | np.ndarray, optional): The position relative to the parent. Defaults to (0, 0).
            angle (float, optional): The rotation angle relative to the parent's angle. Defaults to 0.
            scale (tuple | list | np.ndarray, optional): The scale relative to the parent's scale. Defaults to (1, 1).
            parent (Transform, optional): The parent transform. If None, position, angle and scale will be considered absolut. Defaults to None.
        """
        self.__position : np.ndarray = np.array(position)
        self.__angle : float         = angle
        self.__scale  : np.ndarray   = np.array(scale)
        self.__parent : 'Transform'  = parent
    
    @classmethod
    def fromTransform(self, other : 'Transform') -> 'Transform':
        """
        Copies the values from another Transform.

        Args:
            other (Transform): The Transform to copy. If its none, a standart Transform will be created (pos=(0,0), angle=0, scale=(1,1))

        Returns:
            Transform: The newly created Transform.
        """
        if other is None:
            return Transform()
        else:
            return Transform(other.__position, other.__angle, other.__scale, other.__parent)
    

    def getPosition(self) -> np.ndarray:
        """
        Gets the absolute position. 

        Is influenced by the parent.

        Returns:
            np.ndarray: The absolute position.
        """
        if self.__parent == None:
            return self.__position
        return self.__parent.apply(self.__position)

    def getAngle(self) -> float:
        """
        Gets the absolute rotation angle. 

        Is influenced by the parent.

        Returns:
            np.ndarray: The absolute rotation angle.
        """
        if self.__parent == None:
            return self.__angle
        return self.__angle + self.__parent.getAngle()
    
    def getScale(self) -> np.ndarray:
        """
        Gets the absolute scale. 

        Is influenced by the parent.

        Returns:
            np.ndarray: The absolute scale.
        """
        if self.__parent == None:
            return self.__scale
        return self.__scale * self.__parent.getScale()
    
    def getRelPosition(self) -> np.ndarray:
        """
        Gets the relative position to the parent.

        Is ot influenced by the parent.

        Returns:
            np.ndarray: The relative position.
        """
        return self.__position
    
    def getRelAngle(self) -> float:
        """
        Gets the relative rotation angle to the parent.

        Is ot influenced by the parent.

        Returns:
            np.ndarray: The relative rotation angle.
        """
        return self.__angle

    def getRelScale(self) -> np.ndarray:
        """
        Gets the relative scale to the parent.

        Is ot influenced by the parent.

        Returns:
            np.ndarray: The relative scale.
        """
        return self.__scale

    def translate(self, offset : tuple | list | np.ndarray) -> None:
        """
        Moves the Transform by the offset.

        Args:
            offset (tuple | list | np.ndarray): Moves the Transform by this.
        """
        self.__position += np.array(offset)
    
    def rotate(self, angleOffset : float) -> None:
        """
        Rotates the transform by the angle offset.

        Args:
            angleOffset (float): Rotates the transform by this.
        """
        self.__angle += angleOffset
    
    def scale(self, factor : float | tuple | list | np.ndarray) -> None:
        """
        Scales the transform by the factor.

        Args:
            factor (float | tuple | list | np.ndarray): Scales the transform by that.
        """
        if isinstance(factor, list) or isinstance(factor, tuple):
            factor = np.array(factor)
        self.__scale *= factor
    
    def setRelPosition(self, position : tuple | list | np.ndarray) -> None:
        """
        Sets the relative position to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative position.
        """
        self.__position = np.array(position)
    
    def setRelXPos(self, xPos : float) -> None:
        """
        Sets the relative x coordinate to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative x coordinate.
        """
        self.__position[0] = xPos
    
    def setRelYPos(self, yPos : float) -> None:
        """
        Sets the relative y coordinate to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative y coordinate.
        """
        self.__position[1] = yPos
    
    def setRelAngle(self, angle : float) -> None:
        """
        Sets the relative rotation angle to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative rotation angle.
        """
        self.__angle = angle

    def setRelScale(self, scale : tuple | list | np.ndarray) -> None:
        """
        Sets the relative scale to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative scale.
        """
        self.__scale = np.array(scale)
    
    def setRelXScale(self, xScale : float) -> None:
        """
        Sets the relative x scale to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative x scale.
        """
        self.__scale[0] = xScale
    
    def setRelYScale(self, yScale : float) -> None:
        """
        Sets the relative y scale to the parent.

        Args:
            position (tuple | list | np.ndarray): The new relative y scale.
        """
        self.__scale[1] = yScale
    
    def setParent(self, parent : 'Transform') -> None:
        """
        Sets a new parent of the transform.

        Args:
            parent (Transform): The new parent.
        """
        self.__parent = parent

    def apply(self, vector : tuple | list | np.ndarray) -> np.ndarray:
        """
        Applies the transform to a vector.

        Meaning it will be moved, rotated and scaled.

        Args:
            vector (tuple | list | np.ndarray): The vector, the transform should be applied to.

        Returns:
            np.ndarray: The new transformed vector.
        """
        return np.matmul(Transform.__calcRotationMatrix(self.getAngle()), np.array(vector) * self.getScale()) + self.getPosition()

    def applyMultiple(self, vectors : tuple[np.ndarray] | list[np.ndarray]) -> list[np.ndarray]:
        """
        Applies the transform to a multiple vectors.

        Args:
            vectors (tuple[np.ndarray] | list[np.ndarray]): The vectors, the transform should be applied to.

        Returns:
            np.ndarray: All new transformed vectors.
        """
        return [ self.apply(v) for v in vectors ]
    
    def applyInv(self, vector : tuple | list | np.ndarray) -> np.ndarray:
        """
        Applies the transform inversely.

        Args:
            vector (tuple | list | np.ndarray): The vector, the transform should be applied to inversely.

        Returns:
            np.ndarray: The new transformed vector.
        """
        return np.matmul(Transform.__calcRotationMatrix(-self.getAngle()), np.array(vector) - self.getPosition()) / self.getScale()
    
    def applyInvMultiple(self, vectors : tuple[np.ndarray] | list[np.ndarray]) -> list[np.ndarray]:
        """
        Applies the transform to a multiple vectors inversly.

        Args:
            vectors (tuple[np.ndarray] | list[np.ndarray]): The vectors, the transform should be applied to inversly.

        Returns:
            np.ndarray: All new transformed vectors.
        """
        return [ self.applyInv(v) for v in vectors ]
    
    @classmethod
    def screenCenter(cls, x : float = 512., y : float = 399., angle : float = 0.0, scale : tuple | list | np.ndarray = (1., 1.), parent : 'Transform' = None) -> 'Transform':
        """
        Creates a Component that is in the screen center

        Args:
            x (float, optional): Set this, to overwrite the x coordinate of the resulting Transform. Defaults to 512.
            y (float, optional): Set this, to overwrite the y coordinate of the resulting Transform. Defaults to 399.
            angle (float, optional): The rotation angle relative to the parent's angle. Defaults to 0.
            scale (tuple | list | np.ndarray, optional): The scale relative to the parent's scale. Defaults to (1, 1).
            parent (Transform, optional): The parent transform. If None, position, angle and scale will be considered absolut. Defaults to None.

        Returns:
            Transform: The new centered Transform.
        """
        return cls((x, y), angle, scale, parent)