import os
import pygame
import numpy as np
from pygame import transform

from utils.Transform import Transform

class Images:
    """
    Static class that handles all the graphical resources.
    """

    ROOT_FOLDER = "../../res/img/"
    EXTENTIONS = [ ".png", ".jpg" ]

    __images : dict[str, pygame.Surface]= {}

    @staticmethod
    def loadAll() -> None:
        """
        Loads all graphical resources.
        
        They sould all be in the same folder: ROOT_FOLDER or its subfolders.

        Images that are in subfolders will be accessible via the followign format:
        eg.: ROOT_FOLDER/abc/niceImages/bla.jpg => abc.niceImages.bla
        """
        path = os.path.join(os.path.dirname(__file__), Images.ROOT_FOLDER)
        for root, _, files in os.walk(path):
            for file in files:
                [ filename, extention ] = os.path.splitext(file)
                if extention in Images.EXTENTIONS:
                    key = root[len(path):].replace("\\", ".").replace("/", ".") + "." + filename
                    Images.__images[key] = pygame.image.load(os.path.join(root, file)).convert_alpha()
    
    @staticmethod
    def get(imageKey : str) -> pygame.Surface:
        """
        Gets an image resource as pygame.Surface by its key.

        For the key's structure see Images.loadAll()

        Args:
            imageKey (str): The key of the image.

        Returns:
            pygame.Surface: The resulting surface.
        """
        return Images.__images[imageKey].copy()
    

class Sprite:
    """
    Represents a sprite.

    A sprite is basically an image with a Transform. So it can be directly drawn to the screen at the correct position.
    """

    def __init__(self, image : str | pygame.Surface, transform : Transform = None, enableScaling : bool = False, enableRotation : bool = False, bakeNow : bool = False):
        """
        The constructor of the Sprite class.

        Attention:
            Setting enableScaling and/or enableRotation to true on numerous sprites will drastically lower the games performance as every sprite will be basically drawn twice per frame.

        Args:
            image (str | pygame.Surface): The image the sprite represents.
            transform (Transform, optional): The sprites Transform. Defaults to None.
            enableScaling (bool, optional): Determines whether the scale should be reevaluated every frame. Defaults to False.
            enableRotation (bool, optional): Determines whether the rotation angle should be reevaluated every frame. Defaults to False.
            bakeNow (bool, optional): Determines whether the inital transform should be baked into the Sprite imediately. For details see bakeTransform. Defaults to False.
        """
        self.image : pygame.Surface = Images.get(image) if isinstance(image, str) else image
        self.untransformedImage = self.image.copy()
        self.transform : Transform  = Transform.fromTransform(transform)
        self.enableScaling : bool   = enableScaling
        self.enableRoation : bool   = enableRotation

        if bakeNow:
            self.bakeTransform()

    def bakeTransform(self, includeScale : bool = True, includeRotation : bool = True):
        """
        Bakes the transform to the sprite.

        This is usefull when you want to draw a rotated / scaled image that doesn't rotate and/or scale every frame. 

        Using bakeTransform instead of enableScaling/enableRotation will improve the game's performance.

        Args:
            includeScale (bool, optional): Whether the scale should be considered baking. Defaults to True.
            includeRotation (bool, optional): Whether the rotation angle should be considered baking. Defaults to True.
        """
        self.image = self.untransformedImage.copy()
        if includeScale:
            scale = self.transform.getScale()
            self.image = pygame.transform.flip(self.image, scale[0] < 0, scale[1] < 0)
            self.image = pygame.transform.scale(self.image, np.absolute(scale) * np.array(self.image.get_size()))
        

        if includeRotation:
            self.image = pygame.transform.rotate(self.image, np.degrees(self.transform.getAngle()))

    def draw(self, screen : pygame.Surface) -> None:
        if self.image.get_alpha() == 0:
            return

        img = self.image

        if self.enableScaling:
            scale = self.transform.getScale()
            img = pygame.transform.flip(img, scale[0] < 0, scale[1] < 0)
            img = pygame.transform.scale(img, np.absolute(scale) * np.array(self.image.get_size()))
        

        if self.enableRoation:
            img = pygame.transform.rotate(img, np.degrees(self.transform.getAngle()))

        rect = img.get_rect(center=self.transform.getPosition())
        screen.blit(img, rect)
    
    def unbake(self) -> None:
        """
        Removes any baked transforms from the sprite.
        """
        self.image = self.untransformedImage.copy()
