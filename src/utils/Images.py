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
                    Images.__images[key] = pygame.image.load(os.path.join(root, file))
    
    @staticmethod
    def get(imageKey : str) -> pygame.Surface:
        return Images.__images[imageKey]
    

class Sprite:

    def __init__(self, image : str | pygame.Surface, transform : Transform, enableScaling : bool = False, enableRotation : bool = False):
        self.image = Images.get(image) if isinstance(image, str) else image
        self.transform = transform
        self.enableScaling = enableScaling
        self.enableRoation = enableRotation

    def bakeTransform(self, includeScale : bool = True, includeRotation : bool = True):
        if includeScale:
            scale = self.transform.getScale()
            self.image = pygame.transform.flip(self.image, scale[0] < 0, scale[1] < 0)
            self.image = pygame.transform.scale(self.image, np.absolute(scale) * np.array(self.image.get_size()))
        

        if includeRotation:
            self.image = pygame.transform.rotate(self.image, np.degrees(self.transform.getAngle()))

    def draw(self, screen : pygame.Surface) -> None:
        img = self.image

        if self.enableScaling:
            scale = self.transform.getScale()
            img = pygame.transform.flip(img, scale[0] < 0, scale[1] < 0)
            img = pygame.transform.scale(img, np.absolute(scale) * np.array(self.image.get_size()))
        

        if self.enableRoation:
            img = pygame.transform.rotate(img, np.degrees(self.transform.getAngle()))

        rect = img.get_rect(center=self.transform.getPosition())
        screen.blit(img, rect)
