import pygame
from components.Component import Component
from utils.Images import Sprite


class TargetSelector(Component):
    
    def __init__(self, ownBoardRect : pygame.Rect, oppositeBoardRect : pygame.Rect):
        super().__init__(None)
        self.ownBoardRect = ownBoardRect
        self.oppositeBoardRect = oppositeBoardRect
