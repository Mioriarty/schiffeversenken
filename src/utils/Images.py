import os
import pygame
import numpy as np
from pygame import transform

from utils.Transform import Transform

class Images:

    ROOT_FOLDER = "./res/img/"
    EXTENTIONS = [ ".png", ".jpg" ]

    __images : dict[str, pygame.Surface]= {}

    @staticmethod
    def loadAll() -> None:
        for root, _, files in os.walk(Images.ROOT_FOLDER):
            for file in files:
                [ filename, extention ] = os.path.splitext(file)
                if extention in Images.EXTENTIONS:
                    key = root[len(Images.ROOT_FOLDER):].replace("\\", ".").replace("/", ".") + "." + filename
                    Images.__images[key] = pygame.image.load(os.path.join(root, file)).convert_alpha()
    
    @staticmethod
    def get(imageKey : str) -> pygame.Surface:
        return Images.__images[imageKey].copy()
    

class Sprite:

    def __init__(self, image : str | pygame.Surface, transform : Transform = None, enableScaling : bool = False, enableRotation : bool = False, bakeNow : bool = False):
        self.image : pygame.Surface = Images.get(image) if isinstance(image, str) else image
        self.untransformedImage = self.image.copy()
        self.transform : Transform  = Transform.fromTransform(transform)
        self.enableScaling : bool   = enableScaling
        self.enableRoation : bool   = enableRotation

        if bakeNow:
            self.bakeTransform()

    def bakeTransform(self, includeScale : bool = True, includeRotation : bool = True):
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
